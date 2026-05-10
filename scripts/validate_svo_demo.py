#!/usr/bin/env python3

import argparse
import math
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import cv2
import numpy as np
import rclpy
from nav_msgs.msg import OccupancyGrid, Path as RosPath
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image, PointCloud2
from sensor_msgs_py import point_cloud2


RGB_TOPIC = "/zed/zed_node/rgb/color/rect/image"
INFO_TOPIC = "/zed/zed_node/rgb/color/rect/camera_info"
CLOUD_TOPIC = "/zed/zed_node/point_cloud/cloud_registered"
PATH_TOPIC = "/navivest/path"
GRID_TOPIC = "/navivest/occupancy_grid"


class SampleNode(Node):
    def __init__(self):
        super().__init__("navivest_svo_validation")
        self.latest_image = None
        self.latest_info = None
        self.latest_cloud = None
        self.latest_path = None
        self.latest_grid = None

        self.create_subscription(Image, RGB_TOPIC, self.image_cb, 10)
        self.create_subscription(CameraInfo, INFO_TOPIC, self.info_cb, 10)
        self.create_subscription(PointCloud2, CLOUD_TOPIC, self.cloud_cb, 10)
        self.create_subscription(RosPath, PATH_TOPIC, self.path_cb, 10)
        self.create_subscription(OccupancyGrid, GRID_TOPIC, self.grid_cb, 10)

    def image_cb(self, msg):
        self.latest_image = msg

    def info_cb(self, msg):
        self.latest_info = msg

    def cloud_cb(self, msg):
        self.latest_cloud = msg

    def path_cb(self, msg):
        self.latest_path = msg

    def grid_cb(self, msg):
        self.latest_grid = msg


def image_msg_to_bgr(msg: Image):
    if msg.encoding in ("bgra8", "BGRA8"):
        arr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 4)
        return arr[:, :, :3].copy()
    if msg.encoding in ("rgba8", "RGBA8"):
        arr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 4)
        return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
    if msg.encoding in ("bgr8", "BGR8"):
        return np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3).copy()
    if msg.encoding in ("rgb8", "RGB8"):
        arr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    raise ValueError(f"Unsupported image encoding: {msg.encoding}")


def cloud_xyz(msg: PointCloud2):
    arr = point_cloud2.read_points_numpy(msg, field_names=("x", "y", "z"), skip_nans=False)
    pts = np.asarray(arr, dtype=np.float32).reshape(msg.height, msg.width, 3)
    valid = np.isfinite(pts).all(axis=2) & (pts[:, :, 0] > 0.01)
    return pts, valid


def stamp_seconds(msg):
    return float(msg.header.stamp.sec) + float(msg.header.stamp.nanosec) * 1e-9


def alignment_score(image_msg: Image, cloud_msg: PointCloud2):
    image = image_msg_to_bgr(image_msg)
    _, valid = cloud_xyz(cloud_msg)

    small = cv2.resize(image, (cloud_msg.width, cloud_msg.height), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    rgb_edges = cv2.Canny(gray, 40, 110) > 0

    valid_u8 = valid.astype(np.uint8) * 255
    depth_edges = cv2.morphologyEx(valid_u8, cv2.MORPH_GRADIENT, np.ones((3, 3), dtype=np.uint8)) > 0
    if not np.any(depth_edges):
        return 0.0, float(np.mean(valid)), 0

    rgb_near = cv2.dilate(rgb_edges.astype(np.uint8), np.ones((5, 5), dtype=np.uint8), iterations=1) > 0
    overlap = float(np.count_nonzero(depth_edges & rgb_near) / max(np.count_nonzero(depth_edges), 1))
    return overlap, float(np.mean(valid)), int(np.count_nonzero(depth_edges))


def path_stats(path_msg: RosPath, grid_msg: OccupancyGrid, blindspot_m: float = 0.55):
    poses = path_msg.poses if path_msg is not None else []
    if len(poses) < 2:
        return {
            "path_len": len(poses),
            "path_distance_m": 0.0,
            "starts_at_camera": False,
            "straight_10cm": False,
            "path_unknown_hits": None,
            "path_occ_hits": None,
        }

    pts = np.asarray(
        [(p.pose.position.x, p.pose.position.y, p.pose.position.z) for p in poses],
        dtype=np.float64,
    )
    dist = math.dist(pts[0], pts[-1])
    local_pts = pts
    if grid_msg is not None:
        origin = np.array(
            [
                grid_msg.info.origin.position.x,
                grid_msg.info.origin.position.y,
                grid_msg.info.origin.position.z,
            ],
            dtype=np.float64,
        )
        q = grid_msg.info.origin.orientation
        rot = quaternion_to_matrix(q.x, q.y, q.z, q.w)
        local_pts = (rot.T @ (pts - origin).T).T

    center_y = float(grid_msg.info.height * grid_msg.info.resolution * 0.5) if grid_msg is not None else 0.0
    starts = abs(local_pts[0][0]) < 0.08 and abs(local_pts[0][1] - center_y) < 0.08
    straight = abs(local_pts[1][0] - 0.10) < 0.08 and abs(local_pts[1][1] - center_y) < 0.08

    unknown_hits = 0
    occ_hits = 0
    if grid_msg is not None:
        width = grid_msg.info.width
        height = grid_msg.info.height
        res = grid_msg.info.resolution
        data = np.asarray(grid_msg.data, dtype=np.int16).reshape(height, width)
        for x, y, _ in local_pts:
            if x < blindspot_m:
                continue
            col = int(x / res)
            row = int(y / res)
            if 0 <= row < height and 0 <= col < width:
                val = int(data[row, col])
                unknown_hits += int(val < 0)
                occ_hits += int(val >= 50)

    return {
        "path_len": len(poses),
        "path_distance_m": dist,
        "starts_at_camera": starts,
        "straight_10cm": straight,
        "path_unknown_hits": unknown_hits,
        "path_occ_hits": occ_hits,
    }


def quaternion_to_matrix(x, y, z, w):
    norm = math.sqrt(x * x + y * y + z * z + w * w)
    if norm <= 1e-9:
        return np.eye(3, dtype=np.float64)
    x /= norm
    y /= norm
    z /= norm
    w /= norm

    return np.array(
        [
            [1.0 - 2.0 * (y * y + z * z), 2.0 * (x * y - z * w), 2.0 * (x * z + y * w)],
            [2.0 * (x * y + z * w), 1.0 - 2.0 * (x * x + z * z), 2.0 * (y * z - x * w)],
            [2.0 * (x * z - y * w), 2.0 * (y * z + x * w), 1.0 - 2.0 * (x * x + y * y)],
        ],
        dtype=np.float64,
    )


def grid_stats(grid_msg: OccupancyGrid):
    if grid_msg is None:
        return {"free": 0, "occupied": 0, "unknown": 0}
    data = list(grid_msg.data)
    return {
        "free": data.count(0),
        "occupied": sum(1 for v in data if v >= 50),
        "unknown": data.count(-1),
    }


def camera_model_for(path: Path):
    return "zed" if path.suffix == ".svo" else "zed2i"


def launch_svo(workspace: Path, svo_path: Path, domain_id: int):
    env = os.environ.copy()
    env["ROS_DOMAIN_ID"] = str(domain_id)
    cmd = [
        "bash",
        "-lc",
        "source install/setup.bash && "
        "ros2 launch navivest_bringup navivest_full_svo.launch.py "
        f"svo_path:={svo_path} "
        "guidance_start_m:=0.10 "
        f"camera_model:={camera_model_for(svo_path)} "
        "rviz:=false",
    ]
    return subprocess.Popen(
        cmd,
        cwd=str(workspace),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def collect_samples(sample_count: int, timeout_s: float):
    rclpy.init()
    node = SampleNode()
    samples = []
    last_stamp = None
    end = time.time() + timeout_s

    while time.time() < end and len(samples) < sample_count:
        rclpy.spin_once(node, timeout_sec=0.2)
        if not all((node.latest_image, node.latest_cloud, node.latest_path, node.latest_grid)):
            continue
        if abs(stamp_seconds(node.latest_path) - stamp_seconds(node.latest_grid)) > 0.20:
            continue

        stamp = (
            node.latest_cloud.header.stamp.sec,
            node.latest_cloud.header.stamp.nanosec,
            len(node.latest_path.poses),
        )
        if stamp == last_stamp:
            continue
        last_stamp = stamp

        try:
            align, valid_ratio, edge_count = alignment_score(node.latest_image, node.latest_cloud)
        except Exception as exc:
            align, valid_ratio, edge_count = -1.0, 0.0, 0
            print(f"alignment_error={exc}", file=sys.stderr)

        sample = {
            "alignment": align,
            "cloud_valid_ratio": valid_ratio,
            "cloud_depth_edges": edge_count,
        }
        sample.update(path_stats(node.latest_path, node.latest_grid))
        sample.update({f"grid_{k}": v for k, v in grid_stats(node.latest_grid).items()})
        samples.append(sample)
        time.sleep(0.7)

    node.destroy_node()
    rclpy.shutdown()
    return samples


def summarize_samples(samples):
    if not samples:
        return {
            "samples": 0,
            "alignment_mean": 0.0,
            "cloud_valid_mean": 0.0,
            "path_distance_max": 0.0,
            "path_len_max": 0,
            "unknown_hits_total": 0,
            "occ_hits_total": 0,
            "starts_ok": False,
            "straight_ok": False,
            "free_mean": 0,
            "occupied_mean": 0,
            "unknown_mean": 0,
        }
    return {
        "samples": len(samples),
        "alignment_mean": float(np.mean([s["alignment"] for s in samples])),
        "cloud_valid_mean": float(np.mean([s["cloud_valid_ratio"] for s in samples])),
        "path_distance_max": float(max(s["path_distance_m"] for s in samples)),
        "path_len_max": int(max(s["path_len"] for s in samples)),
        "unknown_hits_total": int(sum(s["path_unknown_hits"] or 0 for s in samples)),
        "occ_hits_total": int(sum(s["path_occ_hits"] or 0 for s in samples)),
        "starts_ok": all(s["starts_at_camera"] for s in samples if s["path_len"] >= 2),
        "straight_ok": all(s["straight_10cm"] for s in samples if s["path_len"] >= 2),
        "free_mean": int(np.mean([s["grid_free"] for s in samples])),
        "occupied_mean": int(np.mean([s["grid_occupied"] for s in samples])),
        "unknown_mean": int(np.mean([s["grid_unknown"] for s in samples])),
    }


def terminate(proc):
    if proc.poll() is not None:
        return
    proc.send_signal(signal.SIGINT)
    try:
        proc.wait(timeout=8)
    except subprocess.TimeoutExpired:
        proc.terminate()
        try:
            proc.wait(timeout=4)
        except subprocess.TimeoutExpired:
            proc.kill()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="/home/macho/navivest_datasets")
    parser.add_argument("--workspace", default="/home/macho/navivest_ws")
    parser.add_argument("--domain-id", type=int, default=77)
    parser.add_argument("--samples", type=int, default=5)
    parser.add_argument("--timeout", type=float, default=14.0)
    args = parser.parse_args()

    workspace = Path(args.workspace)
    svos = sorted(Path(args.dataset).rglob("*.svo")) + sorted(Path(args.dataset).rglob("*.svo2"))
    svos = sorted(svos)
    if not svos:
        raise RuntimeError(f"No SVO files found under {args.dataset}")

    results = []
    for idx, svo in enumerate(svos):
        domain = args.domain_id + idx
        print(f"=== {svo.name} ===", flush=True)
        proc = launch_svo(workspace, svo, domain)
        old_domain = os.environ.get("ROS_DOMAIN_ID")
        os.environ["ROS_DOMAIN_ID"] = str(domain)
        try:
            samples = collect_samples(args.samples, args.timeout)
        finally:
            if old_domain is None:
                os.environ.pop("ROS_DOMAIN_ID", None)
            else:
                os.environ["ROS_DOMAIN_ID"] = old_domain
            terminate(proc)

        summary = summarize_samples(samples)
        summary["file"] = str(svo)
        results.append(summary)
        print(
            "samples={samples} align={alignment_mean:.2f} valid={cloud_valid_mean:.2f} "
            "path_max={path_distance_max:.2f}m len_max={path_len_max} "
            "hits(unk/occ)={unknown_hits_total}/{occ_hits_total} "
            "start={starts_ok} straight10cm={straight_ok} "
            "grid(f/o/u)={free_mean}/{occupied_mean}/{unknown_mean}".format(**summary),
            flush=True,
        )

    bad = [
        r for r in results
        if r["samples"] == 0
        or r["alignment_mean"] < 0.12
        or r["cloud_valid_mean"] < 0.05
        or r["unknown_hits_total"] > 0
        or r["occ_hits_total"] > 0
        or not r["starts_ok"]
        or not r["straight_ok"]
    ]

    print("\n=== Summary ===")
    print(f"files={len(results)} bad={len(bad)}")
    for r in bad:
        print(
            f"CHECK {Path(r['file']).name}: samples={r['samples']} "
            f"align={r['alignment_mean']:.2f} valid={r['cloud_valid_mean']:.2f} "
            f"path={r['path_distance_max']:.2f} occ_hits={r['occ_hits_total']} "
            f"start={r['starts_ok']} straight={r['straight_ok']}"
        )


if __name__ == "__main__":
    main()
