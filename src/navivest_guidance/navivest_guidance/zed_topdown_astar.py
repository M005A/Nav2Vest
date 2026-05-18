#!/usr/bin/env python3

import math
import time
from collections import deque
from typing import Optional, Tuple

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from tf2_ros import Buffer, TransformException, TransformListener

from sensor_msgs.msg import PointCloud2, Image
from sensor_msgs_py import point_cloud2
from nav_msgs.msg import OccupancyGrid, Odometry, Path
from geometry_msgs.msg import Point, PoseStamped
from std_msgs.msg import String
from visualization_msgs.msg import Marker


class ZedTopdownAStar(Node):
    def __init__(self):
        super().__init__("zed_topdown_astar")

        self.declare_parameter("cloud_topic", "/zed/zed_node/point_cloud/cloud_registered")
        self.declare_parameter("odom_topic", "/zed/zed_node/odom")
        self.declare_parameter("grid_frame", "zed_left_camera_frame")
        self.declare_parameter("odom_frame", "odom")

        self.declare_parameter("grid_width_m", 5.0)
        self.declare_parameter("grid_forward_m", 5.0)
        self.declare_parameter("resolution_m", 0.05)

        self.declare_parameter("min_range_m", 0.55)
        self.declare_parameter("guidance_start_m", 0.10)
        # Keep the displayed path anchored under the camera/person, but begin
        # actual obstacle-avoidance routing slightly ahead of that anchor.
        self.declare_parameter("path_start_buffer_m", 0.10)
        self.declare_parameter("max_range_m", 5.0)
        self.declare_parameter("max_abs_lateral_m", 2.5)

        self.declare_parameter("floor_ransac_iters", 120)
        self.declare_parameter("floor_dist_thresh_m", 0.035)
        self.declare_parameter("min_floor_inliers", 1200)
        self.declare_parameter("floor_normal_min_abs_y", 0.55)

        self.declare_parameter("min_obstacle_height_m", 0.07)
        self.declare_parameter("max_obstacle_height_m", 2.20)
        self.declare_parameter("min_obstacle_points_per_cell", 1)
        self.declare_parameter("floor_free_band_m", 0.12)
        self.declare_parameter("free_space_dilation_m", 0.35)
        self.declare_parameter("camera_obstacle_min_down_m", -3.0)
        self.declare_parameter("camera_obstacle_max_down_m", 3.0)
        self.declare_parameter("camera_floor_band_m", 0.12)
        self.declare_parameter("use_camera_axis_fallback", False)
        self.declare_parameter("inflation_radius_m", 0.06)
        self.declare_parameter("planning_inflation_radius_m", 0.06)
        self.declare_parameter("clear_width_m", 0.26)
        self.declare_parameter("obstacle_hold_frames", 6)
        self.declare_parameter("display_obstacle_hold_frames", 1)
        self.declare_parameter("planning_obstacle_hold_frames", 6)
        self.declare_parameter("free_space_hold_frames", 18)
        self.declare_parameter("max_lateral_step_cells", 2)
        self.declare_parameter("path_switch_min_gain_m", 0.55)
        self.declare_parameter("reroute_min_forward_gain_m", 0.75)
        self.declare_parameter("prepend_camera_anchor", True)
        self.declare_parameter("enable_pose_grid_memory", True)
        self.declare_parameter("memory_forward_grid_count", 3)
        self.declare_parameter("memory_lateral_grid_count", 3)
        self.declare_parameter("replan_only_on_grid_exit", True)
        self.declare_parameter("replan_on_path_obstruction", True)
        self.declare_parameter("replan_heading_delta_rad", 0.45)
        self.declare_parameter("new_unit_heading_delta_rad", 0.70)
        self.declare_parameter("active_unit_margin_m", 0.30)
        self.declare_parameter("unit_goal_reached_m", 0.35)

        self.declare_parameter("guidance_topic", "/navivest/guidance")
        self.declare_parameter("stop_path_distance_m", 0.35)
        self.declare_parameter("guidance_first_turn_lookahead_m", 1.10)
        self.declare_parameter("guidance_turn_lateral_threshold_m", 0.15)
        self.declare_parameter("guidance_ignore_near_m", 0.08)
        self.declare_parameter("guidance_debounce_frames", 4)
        self.declare_parameter("guidance_stop_debounce_frames", 2)
        self.declare_parameter("guidance_log_period_s", 0.5)
        self.declare_parameter("invert_guidance_lr", False)

        # Persistent RViz trail of where the camera/person has been.
        # This is published as one growing SPHERE_LIST marker, so points are
        # never deleted during the run.
        self.declare_parameter("camera_trail_topic", "/navivest/camera_trajectory")
        self.declare_parameter("camera_trail_min_distance_m", 0.05)
        self.declare_parameter("camera_trail_point_diameter_m", 0.075)
        self.declare_parameter("camera_trail_z_offset_m", 0.08)

        self.declare_parameter("max_points", 70000)
        self.declare_parameter("max_ransac_points", 12000)
        self.declare_parameter("process_hz", 30.0)
        self.declare_parameter("publish_debug", True)
        self.declare_parameter("debug_scale", 4)
        self.declare_parameter("path_stride_cells", 4)
        self.declare_parameter("stats_period_s", 2.0)

        self.cloud_topic = self.get_parameter("cloud_topic").value

        self.sub = self.create_subscription(
            PointCloud2,
            self.cloud_topic,
            self.cloud_cb,
            qos_profile_sensor_data,
        )
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.odom_topic = str(self.get_parameter("odom_topic").value)
        self.odom_sub = self.create_subscription(
            Odometry,
            self.odom_topic,
            self.odom_cb,
            qos_profile_sensor_data,
        )

        self.grid_pub = self.create_publisher(OccupancyGrid, "/navivest/occupancy_grid", 10)
        self.path_pub = self.create_publisher(Path, "/navivest/path", 10)
        self.debug_pub = self.create_publisher(Image, "/navivest/debug_topdown", 10)
        self.guidance_pub = self.create_publisher(
            String,
            str(self.get_parameter("guidance_topic").value),
            10,
        )
        self.camera_trail_pub = self.create_publisher(
            Marker,
            str(self.get_parameter("camera_trail_topic").value),
            10,
        )

        self.last_plane: Optional[Tuple[np.ndarray, float]] = None
        self.display_obstacle_memory: Optional[np.ndarray] = None
        self.planning_obstacle_memory: Optional[np.ndarray] = None
        self.free_space_memory: Optional[np.ndarray] = None
        self.last_path_cells = []
        self.last_process_time = 0.0
        self.last_log = 0.0
        self.last_stats_log = time.time()
        self.last_guidance_text = ""
        self.pending_guidance_text = ""
        self.pending_guidance_count = 0
        self.last_guidance_log = 0.0
        self.frame_count = 0
        self.pose_xyyaw: Optional[Tuple[float, float, float]] = None
        self.memory_origin_xyyaw: Optional[Tuple[float, float, float]] = None
        self.memory_origin_odom: Optional[np.ndarray] = None
        self.memory_forward_axis: Optional[np.ndarray] = None
        self.memory_right_axis: Optional[np.ndarray] = None
        self.memory_normal_axis: Optional[np.ndarray] = None
        self.current_camera_origin_odom: Optional[np.ndarray] = None
        self.current_floor_origin_odom: Optional[np.ndarray] = None
        self.current_forward_axis: Optional[np.ndarray] = None
        self.current_right_axis: Optional[np.ndarray] = None
        self.current_normal_axis: Optional[np.ndarray] = None
        self.memory_center_segment: Optional[Tuple[int, int]] = None
        self.rolling_planning_grid: Optional[np.ndarray] = None
        self.rolling_display_grid: Optional[np.ndarray] = None
        self.active_unit_segment: Optional[Tuple[int, int]] = None
        self.active_unit_origin_odom: Optional[np.ndarray] = None
        self.active_unit_forward_axis: Optional[np.ndarray] = None
        self.active_unit_right_axis: Optional[np.ndarray] = None
        self.active_path_world = []
        self.active_path_segment: Optional[int] = None
        self.active_path_replan_forward_axis: Optional[np.ndarray] = None
        self.odom_history = deque(maxlen=240)
        self.camera_trail_points = []
        self.last_camera_trail_point: Optional[np.ndarray] = None

        self.get_logger().info(f"Subscribed to {self.cloud_topic}")
        self.get_logger().info(f"Subscribed to {self.odom_topic}")

    def cloud_cb(self, msg: PointCloud2):
        try:
            now = time.perf_counter()
            process_hz = float(self.get_parameter("process_hz").value)
            if process_hz > 0.0 and now - self.last_process_time < 1.0 / process_hz:
                return
            self.last_process_time = now

            pts = self.read_cloud_xyz(msg)
            if pts.shape[0] < 1000:
                self.throttled_warn("Not enough valid cloud points")
                return

            grid, basis, origin = self.build_grid(pts)
            if grid is None:
                return

            grid = self.update_free_space_memory(grid)
            display_grid = self.update_obstacle_memory(
                self.inflate_grid(grid, "inflation_radius_m"),
                "display_obstacle_memory",
                "display_obstacle_hold_frames",
            )
            planning_grid = self.update_obstacle_memory(
                self.inflate_grid(grid, "planning_inflation_radius_m"),
                "planning_obstacle_memory",
                "planning_obstacle_hold_frames",
            )

            odom_tf = self.lookup_camera_pose_transform(msg.header.stamp)
            pose_mode = (
                bool(self.get_parameter("enable_pose_grid_memory").value)
                and odom_tf is not None
                and basis is not None
            )
            segment_changed = False
            if pose_mode:
                self.update_floor_odom_state(basis, origin, odom_tf)
                self.update_camera_trail(msg.header.stamp)
                segment_changed = self.update_rolling_grids(planning_grid, display_grid, basis, origin, odom_tf)
                unit_changed = self.update_active_unit()
                segment_changed = segment_changed or unit_changed
                memory_grid = self.active_unit_grid_from_memory()
                planning_source = memory_grid if memory_grid is not None else planning_grid
                path_cells = self.update_active_world_path(planning_source, segment_changed)
                guidance = self.classify_world_guidance()
            else:
                candidate_path = self.plan_path(planning_grid)
                path_cells = self.stabilize_path(candidate_path, planning_grid)
                guidance = self.classify_guidance(path_cells)

            if pose_mode and self.rolling_display_grid is not None:
                self.publish_rolling_grid(msg)
                self.publish_world_path(msg)
            else:
                self.publish_grid(msg, display_grid, basis)
                self.publish_path(msg, path_cells, basis, origin)
            self.publish_guidance(guidance)
            if bool(self.get_parameter("publish_debug").value):
                self.publish_debug(msg, grid, display_grid, path_cells)
            self.log_stats(time.perf_counter() - now, len(path_cells))

        except Exception as e:
            self.get_logger().error(f"cloud_cb failed: {e}")


    def update_camera_trail(self, stamp):
        """Accumulate a permanent RViz breadcrumb trail of the camera path.

        Uses the current floor-projected camera pose in odom so the trail stays
        aligned with the same world frame as the map/path. Points are only added
        when the camera moves by camera_trail_min_distance_m, and old points are
        intentionally never deleted.
        """
        point = self.current_floor_origin_odom
        if point is None:
            point = self.current_camera_origin_odom
        if point is None:
            return

        point = np.array(point, dtype=np.float64).reshape(3)
        min_dist = float(self.get_parameter("camera_trail_min_distance_m").value)
        if self.last_camera_trail_point is not None:
            if float(np.linalg.norm(point[:2] - self.last_camera_trail_point[:2])) < min_dist:
                self.publish_camera_trail(stamp)
                return

        z_offset = float(self.get_parameter("camera_trail_z_offset_m").value)
        p = Point()
        p.x = float(point[0])
        p.y = float(point[1])
        p.z = float(point[2] + z_offset)
        self.camera_trail_points.append(p)
        self.last_camera_trail_point = point
        self.publish_camera_trail(stamp)

    def publish_camera_trail(self, stamp):
        if not self.camera_trail_points:
            return

        marker = Marker()
        marker.header.frame_id = str(self.get_parameter("odom_frame").value)
        marker.header.stamp = stamp
        marker.ns = "navivest_camera_trajectory"
        marker.id = 0
        marker.type = Marker.SPHERE_LIST
        marker.action = Marker.ADD
        diameter = float(self.get_parameter("camera_trail_point_diameter_m").value)
        marker.scale.x = diameter
        marker.scale.y = diameter
        marker.scale.z = diameter
        marker.color.r = 1.0
        marker.color.g = 0.35
        marker.color.b = 0.0
        marker.color.a = 1.0
        marker.pose.orientation.w = 1.0
        # Keep every point for the whole run. RViz will replace this marker with
        # the same full point list every frame, not delete old points.
        marker.lifetime.sec = 0
        marker.points = list(self.camera_trail_points)
        self.camera_trail_pub.publish(marker)

    def odom_cb(self, msg: Odometry):
        self.odom_history.append(msg)
        q = msg.pose.pose.orientation
        yaw = math.atan2(
            2.0 * (q.w * q.z + q.x * q.y),
            1.0 - 2.0 * (q.y * q.y + q.z * q.z),
        )
        self.pose_xyyaw = (
            float(msg.pose.pose.position.x),
            float(msg.pose.pose.position.y),
            float(yaw),
        )
        if self.memory_origin_xyyaw is None:
            self.memory_origin_xyyaw = self.pose_xyyaw

    def lookup_camera_pose_transform(self, stamp):
        if not self.odom_history:
            return None

        target = rclpy.time.Time.from_msg(stamp).nanoseconds
        best_msg = None
        best_dt = None

        for msg in reversed(self.odom_history):
            if msg.header.stamp.sec == 0 and msg.header.stamp.nanosec == 0:
                continue
            msg_ns = rclpy.time.Time.from_msg(msg.header.stamp).nanoseconds
            dt = abs(target - msg_ns)
            if best_dt is None or dt < best_dt:
                best_dt = dt
                best_msg = msg
            if best_dt is not None and best_dt == 0:
                break

        if best_msg is None:
            return None

        # Skip badly mismatched poses instead of snapping the map to a later TF.
        # A stale transform is worse than a dropped frame for top-down guidance.
        max_skew_ns = int(0.12 * 1e9)
        if best_dt is not None and best_dt > max_skew_ns:
            self.throttled_warn(
                f"Skipping cloud because odom pose is too far from cloud stamp ({best_dt / 1e9:.3f}s)"
            )
            return None

        return self.odom_msg_to_rt(best_msg)

    def odom_msg_to_rt(self, msg: Odometry):
        p = msg.pose.pose.position
        q = msg.pose.pose.orientation
        rot = self.quaternion_to_rotation(q.x, q.y, q.z, q.w)
        trans = np.array([p.x, p.y, p.z], dtype=np.float32)
        return rot, trans

    def lookup_odom_transform(self, source_frame: str, stamp):
        target_frame = str(self.get_parameter("odom_frame").value)
        if not source_frame:
            source_frame = str(self.get_parameter("grid_frame").value)

        try:
            transform = self.tf_buffer.lookup_transform(
                target_frame,
                source_frame,
                rclpy.time.Time.from_msg(stamp),
            )
        except TransformException as exc:
            try:
                transform = self.tf_buffer.lookup_transform(
                    target_frame,
                    source_frame,
                    rclpy.time.Time(),
                )
            except TransformException:
                self.throttled_warn(f"Waiting for TF {target_frame} <- {source_frame}: {exc}")
                return None

        return self.transform_to_rt(transform)

    def transform_to_rt(self, transform):
        t = transform.transform.translation
        q = transform.transform.rotation
        rot = self.quaternion_to_rotation(q.x, q.y, q.z, q.w)
        trans = np.array([t.x, t.y, t.z], dtype=np.float32)
        return rot, trans

    def quaternion_to_rotation(self, x: float, y: float, z: float, w: float) -> np.ndarray:
        xx = x * x
        yy = y * y
        zz = z * z
        xy = x * y
        xz = x * z
        yz = y * z
        wx = w * x
        wy = w * y
        wz = w * z
        return np.array(
            [
                [1.0 - 2.0 * (yy + zz), 2.0 * (xy - wz), 2.0 * (xz + wy)],
                [2.0 * (xy + wz), 1.0 - 2.0 * (xx + zz), 2.0 * (yz - wx)],
                [2.0 * (xz - wy), 2.0 * (yz + wx), 1.0 - 2.0 * (xx + yy)],
            ],
            dtype=np.float32,
        )

    def transform_points(self, points: np.ndarray, odom_tf):
        rot, trans = odom_tf
        return points @ rot.T + trans

    def transform_vector(self, vector: np.ndarray, odom_tf):
        rot, _ = odom_tf
        out = rot @ vector
        return out / max(np.linalg.norm(out), 1e-6)

    def update_floor_odom_state(self, basis, origin: np.ndarray, odom_tf):
        floor_forward, floor_left, floor_normal = basis
        map_y_axis = -floor_left

        _, trans = odom_tf
        fitted_floor_origin = self.transform_points(np.asarray(origin, dtype=np.float32).reshape(1, 3), odom_tf)[0]
        forward_axis = self.transform_vector(floor_forward, odom_tf)
        right_axis = self.transform_vector(map_y_axis, odom_tf)
        normal_axis = self.transform_vector(floor_normal, odom_tf)

        # Anchor the path/grid under the actual camera XY position. The fitted
        # floor plane is still used for height, but its projection is not allowed
        # to slide the camera sideways toward a wall.
        floor_origin = trans.copy()
        floor_origin[2] = fitted_floor_origin[2]

        self.current_camera_origin_odom = trans.copy()
        self.current_floor_origin_odom = floor_origin
        self.current_forward_axis = forward_axis
        self.current_right_axis = right_axis
        self.current_normal_axis = normal_axis

        if self.memory_origin_odom is None:
            self.memory_origin_odom = floor_origin.copy()
            self.memory_forward_axis = forward_axis.copy()
            self.memory_right_axis = right_axis.copy()
            self.memory_normal_axis = normal_axis.copy()

    def read_cloud_xyz(self, msg: PointCloud2) -> np.ndarray:
        arr = point_cloud2.read_points_numpy(
            msg,
            field_names=("x", "y", "z"),
            skip_nans=True,
        )

        pts = np.asarray(arr, dtype=np.float32).reshape(-1, 3)
        pts = pts[np.isfinite(pts).all(axis=1)]

        max_points = int(self.get_parameter("max_points").value)
        if pts.shape[0] > max_points:
            step = int(np.ceil(pts.shape[0] / max_points))
            pts = pts[::step][:max_points]

        return pts

    def build_grid(self, pts: np.ndarray):
        grid_width_m = float(self.get_parameter("grid_width_m").value)
        grid_forward_m = float(self.get_parameter("grid_forward_m").value)
        resolution = float(self.get_parameter("resolution_m").value)
        min_range = float(self.get_parameter("min_range_m").value)
        max_range = float(self.get_parameter("max_range_m").value)
        max_abs_lat = float(self.get_parameter("max_abs_lateral_m").value)

        # In zed_left_camera_frame, the registered cloud uses ROS camera-link
        # style axes: x = forward, y = left, z = up.
        forward = pts[:, 0]
        lateral = pts[:, 1]

        roi = (
            (forward > min_range)
            & (forward < max_range)
            & (np.abs(lateral) < max_abs_lat)
        )
        pts_roi = pts[roi]

        if pts_roi.shape[0] < 1000:
            self.throttled_warn("ROI has too few points")
            return None, None, None

        plane = self.fit_floor_plane(pts_roi)
        if plane is None:
            self.throttled_warn("No floor plane found")
            return None, None, None

        n, d = plane

        # Make camera origin be above floor.
        if d < 0:
            n = -n
            d = -d

        self.last_plane = (n, d)

        camera_forward = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        floor_forward = camera_forward - np.dot(camera_forward, n) * n
        norm = np.linalg.norm(floor_forward)

        if norm < 1e-4:
            floor_forward = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        else:
            floor_forward = floor_forward / norm

        floor_left = np.cross(n, floor_forward)
        floor_left = floor_left / max(np.linalg.norm(floor_left), 1e-6)

        heights = pts_roi @ n + d
        x_forward = pts_roi @ floor_forward
        y_left = pts_roi @ floor_left
        y_grid = -y_left

        min_h = float(self.get_parameter("min_obstacle_height_m").value)
        max_h = float(self.get_parameter("max_obstacle_height_m").value)

        rows = int(grid_forward_m / resolution)
        cols = int(grid_width_m / resolution)

        grid = np.full((rows, cols), 255, dtype=np.uint8)

        floor_band = float(self.get_parameter("floor_free_band_m").value)
        floor = (
            (heights > -floor_band)
            & (heights < min_h)
            & (x_forward > min_range)
            & (x_forward < grid_forward_m)
            & (np.abs(y_grid) < grid_width_m / 2.0)
        )
        self.mark_free_points(
            grid,
            x_forward[floor],
            y_grid[floor],
            grid_width_m,
            resolution,
        )

        obs = (
            (heights > min_h)
            & (heights < max_h)
            & (x_forward > min_range)
            & (x_forward < grid_forward_m)
            & (np.abs(y_grid) < grid_width_m / 2.0)
        )
        obs_x = x_forward[obs]
        obs_y = y_grid[obs]
        self.mark_obstacle_points(grid, obs_x, obs_y, grid_width_m, resolution)

        if bool(self.get_parameter("use_camera_axis_fallback").value):
            cam_obs = self.camera_axis_obstacles(
                pts_roi,
                min_range,
                grid_forward_m,
                grid_width_m,
            )
            self.mark_obstacle_points(
                grid,
                cam_obs[:, 0],
                cam_obs[:, 1],
                grid_width_m,
                resolution,
            )

        basis = (floor_forward, floor_left, n)
        # Floor-frame origin is the camera origin projected onto the fitted
        # floor. This keeps the top-down chart aligned with the 3D cloud even
        # when the chest-mounted camera is pitched downward.
        origin = -d * n

        return grid, basis, origin

    def mark_free_points(
        self,
        grid: np.ndarray,
        forward_m: np.ndarray,
        left_m: np.ndarray,
        grid_width_m: float,
        resolution: float,
    ):
        rows, cols = grid.shape
        gx = (forward_m / resolution).astype(np.int32)
        gy = ((left_m + grid_width_m / 2.0) / resolution).astype(np.int32)

        valid = (gx >= 0) & (gx < rows) & (gy >= 0) & (gy < cols)
        gx = gx[valid]
        gy = gy[valid]
        if gx.size == 0:
            return

        observed = np.zeros_like(grid, dtype=np.uint8)
        observed[gx, gy] = 255

        dilation_m = float(self.get_parameter("free_space_dilation_m").value)
        if dilation_m > 0.0:
            radius = max(1, int(round(dilation_m / resolution)))
            kernel = cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE,
                (2 * radius + 1, 2 * radius + 1),
            )
            observed = cv2.dilate(observed, kernel, iterations=1)

        grid[observed > 0] = 0

    def camera_axis_obstacles(
        self,
        pts: np.ndarray,
        min_range: float,
        grid_forward_m: float,
        grid_width_m: float,
    ) -> np.ndarray:
        floor_band = float(self.get_parameter("camera_floor_band_m").value)
        min_down = float(self.get_parameter("camera_obstacle_min_down_m").value)
        max_down = float(self.get_parameter("camera_obstacle_max_down_m").value)

        # Fallback for frames where the floor plane is noisy: reject the floor
        # band in raw camera coordinates and mark remaining above-floor points.
        z_up = pts[:, 2]
        forward = pts[:, 0]
        lateral = pts[:, 1]
        floor_z = np.nanpercentile(z_up, 12.0)

        obs = (
            (forward > min_range)
            & (forward < grid_forward_m)
            & (np.abs(lateral) < grid_width_m / 2.0)
            & (z_up > min_down)
            & (z_up < max_down)
            & (z_up > floor_z + floor_band)
        )
        return pts[obs]

    def mark_obstacle_points(
        self,
        grid: np.ndarray,
        forward_m: np.ndarray,
        left_m: np.ndarray,
        grid_width_m: float,
        resolution: float,
    ):
        rows, cols = grid.shape
        gx = (forward_m / resolution).astype(np.int32)
        gy = ((left_m + grid_width_m / 2.0) / resolution).astype(np.int32)

        valid = (gx >= 0) & (gx < rows) & (gy >= 0) & (gy < cols)
        gx = gx[valid]
        gy = gy[valid]
        if gx.size == 0:
            return

        min_count = max(1, int(self.get_parameter("min_obstacle_points_per_cell").value))
        if min_count <= 1:
            grid[gx, gy] = 100
            return

        flat = gx * cols + gy
        counts = np.bincount(flat, minlength=rows * cols)
        occupied = counts.reshape(rows, cols) >= min_count
        grid[occupied] = 100

    def fit_floor_plane(self, pts: np.ndarray):
        iters = int(self.get_parameter("floor_ransac_iters").value)
        thresh = float(self.get_parameter("floor_dist_thresh_m").value)
        min_inliers = int(self.get_parameter("min_floor_inliers").value)
        min_abs_y = float(self.get_parameter("floor_normal_min_abs_y").value)

        best_n = None
        best_d = 0.0
        best_count = 0

        if pts.shape[0] < 500:
            return None

        max_ransac_points = int(self.get_parameter("max_ransac_points").value)
        if pts.shape[0] > max_ransac_points:
            step = int(np.ceil(pts.shape[0] / max_ransac_points))
            plane_pts = pts[::step][:max_ransac_points]
        else:
            plane_pts = pts

        for _ in range(iters):
            ids = np.random.randint(0, plane_pts.shape[0], size=3)
            p1, p2, p3 = plane_pts[ids]

            n = np.cross(p2 - p1, p3 - p1)
            norm = np.linalg.norm(n)
            if norm < 1e-6:
                continue

            n = n / norm
            d = -np.dot(n, p1)

            # In the ZED left camera frame, Z is the vertical-ish axis.
            # Reject wall-like planes so chair/wall points are not mistaken for floor.
            vertical_alignment = abs(float(n[2]))
            if vertical_alignment < min_abs_y:
                continue

            dist = np.abs(plane_pts @ n + d)
            count = int(np.count_nonzero(dist < thresh))

            # Prefer planes below the camera and with many inliers. For an
            # upward-facing floor normal, d is positive when the floor is below
            # the camera origin.
            if d > 0:
                score = int(count * vertical_alignment)
            else:
                score = int(count * vertical_alignment * 0.8)

            if score > best_count:
                best_count = score
                best_n = n.astype(np.float32)
                best_d = float(d)

        if best_n is None or best_count < min_inliers:
            return None

        # Smooth plane to avoid jitter.
        if self.last_plane is not None:
            old_n, old_d = self.last_plane
            if np.dot(old_n, best_n) < 0:
                best_n = -best_n
                best_d = -best_d

            alpha = 0.85
            best_n = alpha * old_n + (1.0 - alpha) * best_n
            best_n = best_n / max(np.linalg.norm(best_n), 1e-6)
            best_d = alpha * old_d + (1.0 - alpha) * best_d

        return best_n, best_d

    def inflate_grid(self, grid: np.ndarray, radius_parameter: str) -> np.ndarray:
        resolution = float(self.get_parameter("resolution_m").value)
        inflation_radius = float(self.get_parameter(radius_parameter).value)
        if inflation_radius <= 0.0:
            return grid.copy()
        r = max(1, int(inflation_radius / resolution))

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
        occ = (grid == 100).astype(np.uint8) * 255
        inflated = cv2.dilate(occ, kernel)

        out = grid.copy()
        out[inflated > 0] = 100
        return out

    def update_obstacle_memory(
        self,
        grid: np.ndarray,
        memory_attr: str,
        hold_parameter: str,
    ) -> np.ndarray:
        hold_frames = int(self.get_parameter(hold_parameter).value)
        if hold_frames <= 0:
            return grid

        memory = getattr(self, memory_attr)
        if memory is None or memory.shape != grid.shape:
            memory = np.zeros_like(grid, dtype=np.uint8)

        memory[memory > 0] -= 1
        memory[grid == 100] = np.uint8(min(hold_frames, 255))
        setattr(self, memory_attr, memory)

        out = grid.copy()
        out[memory > 0] = 100
        return out

    def update_free_space_memory(self, grid: np.ndarray) -> np.ndarray:
        hold_frames = int(self.get_parameter("free_space_hold_frames").value)
        if hold_frames <= 0:
            return grid

        if self.free_space_memory is None or self.free_space_memory.shape != grid.shape:
            self.free_space_memory = np.zeros_like(grid, dtype=np.uint8)

        self.free_space_memory[self.free_space_memory > 0] -= 1
        self.free_space_memory[grid == 0] = np.uint8(min(hold_frames, 255))

        out = grid.copy()
        out[self.free_space_memory > 0] = 0
        out[grid == 100] = 100
        return out

    def current_memory_segment(self) -> Optional[int]:
        segment = self.current_memory_segment_2d()
        if segment is None:
            return None
        return segment[0]

    def current_memory_segment_2d(self) -> Optional[Tuple[int, int]]:
        if (
            self.current_camera_origin_odom is None
            or self.memory_origin_odom is None
            or self.memory_forward_axis is None
            or self.memory_right_axis is None
        ):
            return None

        rel = self.current_camera_origin_odom - self.memory_origin_odom
        progress = float(np.dot(rel, self.memory_forward_axis))
        lateral = float(np.dot(rel, self.memory_right_axis))
        segment_len = float(self.get_parameter("grid_forward_m").value)
        grid_width_m = float(self.get_parameter("grid_width_m").value)
        if segment_len <= 0.0 or grid_width_m <= 0.0:
            return (0, 0)
        return (
            int(math.floor(progress / segment_len)),
            int(math.floor((lateral + grid_width_m / 2.0) / grid_width_m)),
        )

    def ensure_rolling_memory(self, segment: int, shape) -> bool:
        rows, cols = shape
        forward_count = max(3, int(self.get_parameter("memory_forward_grid_count").value))
        lateral_count = max(3, int(self.get_parameter("memory_lateral_grid_count").value))
        if forward_count % 2 == 0:
            forward_count += 1
        if lateral_count % 2 == 0:
            lateral_count += 1

        expected_shape = (rows * forward_count, cols * lateral_count)
        if self.rolling_planning_grid is None or self.rolling_planning_grid.shape != expected_shape:
            self.rolling_planning_grid = np.full(expected_shape, 255, dtype=np.uint8)
            self.rolling_display_grid = np.full(expected_shape, 255, dtype=np.uint8)
            self.memory_center_segment = segment
            return True

        if self.memory_center_segment is None:
            self.memory_center_segment = segment
            return True

        delta_forward = segment[0] - self.memory_center_segment[0]
        delta_lateral = segment[1] - self.memory_center_segment[1]
        if delta_forward == 0 and delta_lateral == 0:
            return False

        if abs(delta_forward) >= forward_count or abs(delta_lateral) >= lateral_count:
            self.rolling_planning_grid.fill(255)
            self.rolling_display_grid.fill(255)
        else:
            self.shift_memory(delta_forward, delta_lateral, rows, cols)

        self.memory_center_segment = segment
        return True

    def shift_memory(self, delta_forward: int, delta_lateral: int, rows: int, cols: int):
        row_shift = delta_forward * rows
        col_shift = delta_lateral * cols

        for memory in (self.rolling_planning_grid, self.rolling_display_grid):
            old = memory.copy()
            memory.fill(255)
            src_r0 = max(0, row_shift)
            src_r1 = min(old.shape[0], old.shape[0] + row_shift)
            dst_r0 = max(0, -row_shift)
            dst_r1 = dst_r0 + max(0, src_r1 - src_r0)
            src_c0 = max(0, col_shift)
            src_c1 = min(old.shape[1], old.shape[1] + col_shift)
            dst_c0 = max(0, -col_shift)
            dst_c1 = dst_c0 + max(0, src_c1 - src_c0)
            if dst_r1 > dst_r0 and dst_c1 > dst_c0:
                memory[dst_r0:dst_r1, dst_c0:dst_c1] = old[src_r0:src_r1, src_c0:src_c1]

    def update_rolling_grids(self, planning_grid: np.ndarray, display_grid: np.ndarray, basis, origin, odom_tf) -> bool:
        segment = self.current_memory_segment_2d()
        if segment is None:
            return False

        segment_changed = self.ensure_rolling_memory(segment, planning_grid.shape)
        self.insert_local_grid_into_memory(planning_grid, self.rolling_planning_grid, basis, origin, odom_tf)
        self.insert_local_grid_into_memory(display_grid, self.rolling_display_grid, basis, origin, odom_tf)
        return segment_changed

    def insert_local_grid_into_memory(self, local_grid: np.ndarray, memory_grid: Optional[np.ndarray], basis, origin, odom_tf):
        if (
            memory_grid is None
            or self.memory_origin_odom is None
            or self.memory_forward_axis is None
            or self.memory_right_axis is None
            or self.memory_center_segment is None
        ):
            return

        rows, cols = local_grid.shape
        resolution = float(self.get_parameter("resolution_m").value)
        grid_width_m = float(self.get_parameter("grid_width_m").value)
        segment_len = float(self.get_parameter("grid_forward_m").value)
        forward_count = max(3, int(self.get_parameter("memory_forward_grid_count").value))
        lateral_count = max(3, int(self.get_parameter("memory_lateral_grid_count").value))
        if forward_count % 2 == 0:
            forward_count += 1
        if lateral_count % 2 == 0:
            lateral_count += 1
        first_forward_segment = self.memory_center_segment[0] - forward_count // 2
        first_lateral_segment = self.memory_center_segment[1] - lateral_count // 2

        observed = np.argwhere(local_grid != 255)
        if observed.size == 0:
            return

        r = observed[:, 0].astype(np.float32)
        c = observed[:, 1].astype(np.float32)
        forward = r * resolution
        side_right = c * resolution - grid_width_m / 2.0

        local_points = self.local_cells_to_frame_points(forward, side_right, basis, origin)
        world = self.transform_points(local_points, odom_tf)
        rel = world - self.memory_origin_odom
        progress = rel @ self.memory_forward_axis
        lateral = rel @ self.memory_right_axis

        mem_rows = ((progress - first_forward_segment * segment_len) / resolution).astype(np.int32)
        lateral_origin = first_lateral_segment * grid_width_m - grid_width_m / 2.0
        mem_cols = ((lateral - lateral_origin) / resolution).astype(np.int32)
        valid = (
            (mem_rows >= 0)
            & (mem_rows < memory_grid.shape[0])
            & (mem_cols >= 0)
            & (mem_cols < memory_grid.shape[1])
        )
        if not np.any(valid):
            return

        vals = local_grid[observed[valid, 0], observed[valid, 1]]
        rr = mem_rows[valid]
        cc = mem_cols[valid]
        memory_grid[rr[vals == 0], cc[vals == 0]] = 0
        memory_grid[rr[vals == 100], cc[vals == 100]] = 100

    def camera_grid_from_memory(self) -> Optional[np.ndarray]:
        if (
            self.rolling_planning_grid is None
            or self.current_floor_origin_odom is None
            or self.current_forward_axis is None
            or self.current_right_axis is None
            or self.memory_origin_odom is None
            or self.memory_forward_axis is None
            or self.memory_right_axis is None
            or self.memory_center_segment is None
        ):
            return None

        rows = int(float(self.get_parameter("grid_forward_m").value) / float(self.get_parameter("resolution_m").value))
        cols = int(float(self.get_parameter("grid_width_m").value) / float(self.get_parameter("resolution_m").value))
        resolution = float(self.get_parameter("resolution_m").value)
        grid_width_m = float(self.get_parameter("grid_width_m").value)
        segment_len = float(self.get_parameter("grid_forward_m").value)
        forward_count = max(3, int(self.get_parameter("memory_forward_grid_count").value))
        lateral_count = max(3, int(self.get_parameter("memory_lateral_grid_count").value))
        if forward_count % 2 == 0:
            forward_count += 1
        if lateral_count % 2 == 0:
            lateral_count += 1
        first_forward_segment = self.memory_center_segment[0] - forward_count // 2
        first_lateral_segment = self.memory_center_segment[1] - lateral_count // 2

        rr, cc = np.indices((rows, cols), dtype=np.float32)
        forward = rr * resolution
        side_right = cc * resolution - grid_width_m / 2.0

        world = (
            self.current_camera_origin_odom
            + forward[..., None] * self.current_forward_axis
            + side_right[..., None] * self.current_right_axis
        )
        rel = world - self.memory_origin_odom
        progress = rel @ self.memory_forward_axis
        lateral = rel @ self.memory_right_axis
        mem_rows = ((progress - first_forward_segment * segment_len) / resolution).astype(np.int32)
        lateral_origin = first_lateral_segment * grid_width_m - grid_width_m / 2.0
        mem_cols = ((lateral - lateral_origin) / resolution).astype(np.int32)

        out = np.full((rows, cols), 255, dtype=np.uint8)
        valid = (
            (mem_rows >= 0)
            & (mem_rows < self.rolling_planning_grid.shape[0])
            & (mem_cols >= 0)
            & (mem_cols < self.rolling_planning_grid.shape[1])
        )
        out[valid] = self.rolling_planning_grid[mem_rows[valid], mem_cols[valid]]
        return out

    def active_unit_grid_from_memory(self) -> Optional[np.ndarray]:
        if (
            self.active_unit_segment is None
            or self.active_unit_origin_odom is None
            or self.active_unit_forward_axis is None
            or self.active_unit_right_axis is None
        ):
            return None

        return self.grid_from_memory(
            self.active_unit_segment,
            self.active_unit_origin_odom,
            self.active_unit_forward_axis,
            self.active_unit_right_axis,
        )

    def grid_from_memory(
        self,
        segment: Tuple[int, int],
        origin_odom: np.ndarray,
        forward_axis: np.ndarray,
        right_axis: np.ndarray,
    ) -> Optional[np.ndarray]:
        if (
            self.rolling_planning_grid is None
            or self.memory_origin_odom is None
            or self.memory_forward_axis is None
            or self.memory_right_axis is None
            or self.memory_center_segment is None
        ):
            return None

        rows = int(float(self.get_parameter("grid_forward_m").value) / float(self.get_parameter("resolution_m").value))
        cols = int(float(self.get_parameter("grid_width_m").value) / float(self.get_parameter("resolution_m").value))
        resolution = float(self.get_parameter("resolution_m").value)
        grid_width_m = float(self.get_parameter("grid_width_m").value)
        segment_len = float(self.get_parameter("grid_forward_m").value)
        forward_count = max(3, int(self.get_parameter("memory_forward_grid_count").value))
        lateral_count = max(3, int(self.get_parameter("memory_lateral_grid_count").value))
        if forward_count % 2 == 0:
            forward_count += 1
        if lateral_count % 2 == 0:
            lateral_count += 1
        first_forward_segment = self.memory_center_segment[0] - forward_count // 2
        first_lateral_segment = self.memory_center_segment[1] - lateral_count // 2
        if not (first_forward_segment <= segment[0] < first_forward_segment + forward_count):
            return None
        if not (first_lateral_segment <= segment[1] < first_lateral_segment + lateral_count):
            return None

        rr, cc = np.indices((rows, cols), dtype=np.float32)
        forward = rr * resolution
        side_right = cc * resolution - grid_width_m / 2.0
        world = origin_odom + forward[..., None] * forward_axis + side_right[..., None] * right_axis
        rel = world - self.memory_origin_odom
        progress = rel @ self.memory_forward_axis
        lateral = rel @ self.memory_right_axis
        mem_rows = ((progress - first_forward_segment * segment_len) / resolution).astype(np.int32)
        lateral_origin = first_lateral_segment * grid_width_m - grid_width_m / 2.0
        mem_cols = ((lateral - lateral_origin) / resolution).astype(np.int32)

        out = np.full((rows, cols), 255, dtype=np.uint8)
        valid = (
            (mem_rows >= 0)
            & (mem_rows < self.rolling_planning_grid.shape[0])
            & (mem_cols >= 0)
            & (mem_cols < self.rolling_planning_grid.shape[1])
        )
        out[valid] = self.rolling_planning_grid[mem_rows[valid], mem_cols[valid]]
        return out

    def current_unit_grid_from_memory(self) -> Optional[np.ndarray]:
        return self.active_unit_grid_from_memory()

    def memory_slice_bounds(self, segment: Tuple[int, int], memory_shape) -> Optional[Tuple[int, int, int, int]]:
        rows = int(float(self.get_parameter("grid_forward_m").value) / float(self.get_parameter("resolution_m").value))
        cols = int(float(self.get_parameter("grid_width_m").value) / float(self.get_parameter("resolution_m").value))
        grid_width_m = float(self.get_parameter("grid_width_m").value)
        if rows <= 0 or cols <= 0 or grid_width_m <= 0.0:
            return None

        forward_count = max(3, int(self.get_parameter("memory_forward_grid_count").value))
        lateral_count = max(3, int(self.get_parameter("memory_lateral_grid_count").value))
        if forward_count % 2 == 0:
            forward_count += 1
        if lateral_count % 2 == 0:
            lateral_count += 1

        first_forward_segment = self.memory_center_segment[0] - forward_count // 2
        first_lateral_segment = self.memory_center_segment[1] - lateral_count // 2
        seg_row = segment[0] - first_forward_segment
        seg_col = segment[1] - first_lateral_segment
        if not (0 <= seg_row < forward_count and 0 <= seg_col < lateral_count):
            return None

        r0 = seg_row * rows
        c0 = seg_col * cols
        r1 = r0 + rows
        c1 = c0 + cols
        if r1 > memory_shape[0] or c1 > memory_shape[1]:
            return None
        return r0, r1, c0, c1

    def current_unit_origin_odom(self) -> Optional[np.ndarray]:
        if (
            self.active_unit_segment is None
            or self.memory_origin_odom is None
            or self.memory_forward_axis is None
            or self.memory_right_axis is None
        ):
            return None

        return self.segment_origin_odom(self.active_unit_segment)

    def segment_origin_odom(self, segment: Tuple[int, int]) -> Optional[np.ndarray]:
        if (
            self.memory_origin_odom is None
            or self.memory_forward_axis is None
            or self.memory_right_axis is None
        ):
            return None

        segment_len = float(self.get_parameter("grid_forward_m").value)
        grid_width_m = float(self.get_parameter("grid_width_m").value)
        return (
            self.memory_origin_odom
            + self.memory_forward_axis * (segment[0] * segment_len)
            + self.memory_right_axis * (segment[1] * grid_width_m - grid_width_m / 2.0)
        )

    def update_active_unit(self, current_segment: Optional[Tuple[int, int]] = None) -> bool:
        if (
            self.current_floor_origin_odom is None
            or self.current_forward_axis is None
            or self.current_right_axis is None
        ):
            return False

        if current_segment is None:
            current_segment = self.current_memory_segment_2d()
        if current_segment is None:
            return False

        # No active unit yet: freeze a local planning frame from the camera's
        # current floor pose and current heading. The rolling memory can stay in
        # its original odom axes; grid_from_memory() samples that memory into
        # this active unit frame.
        if self.active_unit_segment is None:
            self.set_active_unit(current_segment)
            return True

        # If the person intentionally turns, the old unit-forward direction is
        # no longer the direction guidance should plan toward. Start a new unit
        # at the current camera pose/heading instead of continuing to plan
        # "up" in the old grid.
        if self.active_unit_heading_stale():
            self.set_active_unit(current_segment)
            return True

        # If the camera has walked out of the frozen unit bounds, advance/reset
        # the unit. This catches both normal forward progress and side exits.
        if self.camera_outside_active_unit() or self.camera_reached_active_unit_end():
            self.set_active_unit(current_segment)
            return True

        # Keep origin and axes frozen while inside the unit. Do NOT overwrite
        # them with global memory axes every frame, otherwise the path always
        # points in the original "up" direction.
        return False

    def set_active_unit(self, segment: Tuple[int, int]):
        self.active_unit_segment = segment
        self.active_unit_origin_odom = (
            None if self.current_floor_origin_odom is None else self.current_floor_origin_odom.copy()
        )
        self.active_unit_forward_axis = (
            None if self.current_forward_axis is None else self.current_forward_axis.copy()
        )
        self.active_unit_right_axis = (
            None if self.current_right_axis is None else self.current_right_axis.copy()
        )
        self.active_path_world = []
        self.active_path_segment = None
        self.active_path_replan_forward_axis = None
        self.last_path_cells = []

    def active_unit_heading_stale(self) -> bool:
        if self.active_unit_forward_axis is None or self.current_forward_axis is None:
            return False
        dot = float(np.clip(np.dot(self.active_unit_forward_axis, self.current_forward_axis), -1.0, 1.0))
        delta = math.acos(dot)
        threshold = float(self.get_parameter("new_unit_heading_delta_rad").value)
        return delta >= threshold

    def camera_cell_in_active_unit(self):
        if (
            self.current_floor_origin_odom is None
            or self.active_unit_origin_odom is None
            or self.active_unit_forward_axis is None
            or self.active_unit_right_axis is None
        ):
            return None
        resolution = float(self.get_parameter("resolution_m").value)
        grid_width_m = float(self.get_parameter("grid_width_m").value)
        rel = self.current_floor_origin_odom - self.active_unit_origin_odom
        forward_m = float(np.dot(rel, self.active_unit_forward_axis))
        side_m = float(np.dot(rel, self.active_unit_right_axis))
        row = int(math.floor(forward_m / resolution))
        col = int(math.floor((side_m + grid_width_m / 2.0) / resolution))
        return row, col, forward_m, side_m

    def camera_outside_active_unit(self) -> bool:
        cell = self.camera_cell_in_active_unit()
        if cell is None:
            return False
        _, _, forward_m, side_m = cell
        unit_len = float(self.get_parameter("grid_forward_m").value)
        grid_width_m = float(self.get_parameter("grid_width_m").value)
        margin = float(self.get_parameter("active_unit_margin_m").value)
        return (
            forward_m < -margin
            or forward_m > unit_len + margin
            or abs(side_m) > grid_width_m / 2.0 + margin
        )

    def camera_reached_active_unit_end(self) -> bool:
        cell = self.camera_cell_in_active_unit()
        if cell is None:
            return False

        unit_len = float(self.get_parameter("grid_forward_m").value)
        threshold = float(self.get_parameter("unit_goal_reached_m").value)
        _, _, forward_progress, _ = cell
        remaining = unit_len - forward_progress
        return remaining <= threshold

    def local_cells_to_frame_points(self, forward_m, side_m, basis, origin):
        floor_forward, floor_left, _ = basis
        map_y_axis = -floor_left
        return (
            np.asarray(origin, dtype=np.float32)
            + np.asarray(forward_m, dtype=np.float32)[:, None] * floor_forward[None, :]
            + np.asarray(side_m, dtype=np.float32)[:, None] * map_y_axis[None, :]
        )

    def stabilize_path(self, candidate_path, planning_grid):
        if not candidate_path:
            return self.last_path_cells

        if not self.last_path_cells:
            self.last_path_cells = candidate_path
            return candidate_path

        resolution = float(self.get_parameter("resolution_m").value)
        clear_width = float(self.get_parameter("clear_width_m").value)
        half_width_cells = max(1, int(round((clear_width * 0.5) / resolution)))

        if not self.path_is_clear(self.last_path_cells, planning_grid, half_width_cells):
            self.last_path_cells = candidate_path
            return candidate_path

        old_gain = self.forward_gain(self.last_path_cells)
        new_gain = self.forward_gain(candidate_path)
        min_gain = float(self.get_parameter("path_switch_min_gain_m").value)

        if new_gain <= old_gain + min_gain:
            return self.last_path_cells

        self.last_path_cells = candidate_path
        return candidate_path

    def update_active_world_path(self, planning_grid: np.ndarray, segment_changed: bool):
        current_cells = self.world_path_to_unit_cells(self.active_path_world)
        path_obstructed = (
            bool(self.get_parameter("replan_on_path_obstruction").value)
            and self.active_path_world
            and not self.local_path_is_clear(current_cells, planning_grid)
        )
        heading_changed = self.active_path_heading_stale()

        candidate_path = self.plan_path(planning_grid)
        candidate_world = self.path_cells_to_world(candidate_path)
        checked_path = candidate_path[1:] if len(candidate_path) > 2 else candidate_path
        candidate_valid = (
            len(candidate_world) >= 2
            and self.forward_gain(candidate_path) > 0.0
            and self.local_path_is_clear(checked_path, planning_grid)
        )

        if candidate_valid:
            # Replan every processed cloud, but only replace the displayed path
            # when the new path is usable. This keeps the last known-good route
            # through brief depth or floor-plane dropouts.
            self.active_path_world = candidate_world
            self.active_path_segment = self.active_unit_segment
            self.active_path_replan_forward_axis = (
                None if self.current_forward_axis is None else self.current_forward_axis.copy()
            )
            return candidate_path

        if not self.active_path_world or path_obstructed or heading_changed or segment_changed:
            return current_cells

        return current_cells

    def path_cells_to_world(self, path_cells):
        if (
            self.active_unit_origin_odom is None
            or self.active_unit_forward_axis is None
            or self.active_unit_right_axis is None
        ):
            return []

        resolution = float(self.get_parameter("resolution_m").value)
        grid_width_m = float(self.get_parameter("grid_width_m").value)

        out = []
        for row, col in path_cells:
            forward_m = row * resolution
            side_m = col * resolution - grid_width_m / 2.0
            point = (
                self.active_unit_origin_odom
                + self.active_unit_forward_axis * forward_m
                + self.active_unit_right_axis * side_m
            )
            out.append((float(point[0]), float(point[1]), float(point[2])))
        return out

    def world_path_to_unit_cells(self, world_path):
        if (
            self.active_unit_origin_odom is None
            or self.active_unit_forward_axis is None
            or self.active_unit_right_axis is None
        ):
            return []

        rows = int(float(self.get_parameter("grid_forward_m").value) / float(self.get_parameter("resolution_m").value))
        cols = int(float(self.get_parameter("grid_width_m").value) / float(self.get_parameter("resolution_m").value))
        resolution = float(self.get_parameter("resolution_m").value)
        grid_width_m = float(self.get_parameter("grid_width_m").value)

        cells = []
        for point in world_path:
            rel = np.array(point, dtype=np.float32) - self.active_unit_origin_odom
            forward_m = float(np.dot(rel, self.active_unit_forward_axis))
            side_m = float(np.dot(rel, self.active_unit_right_axis))
            row = int(round(forward_m / resolution))
            col = int(round((side_m + grid_width_m / 2.0) / resolution))
            if 0 <= row < rows and 0 <= col < cols:
                cells.append((row, col))
        return self.decimate_path(cells)

    def local_path_is_clear(self, path_cells, grid) -> bool:
        if len(path_cells) < 2:
            return False

        resolution = float(self.get_parameter("resolution_m").value)
        clear_width = float(self.get_parameter("clear_width_m").value)
        half_width_cells = max(1, int(round((clear_width * 0.5) / resolution)))
        return self.path_is_clear(path_cells, grid, half_width_cells)

    def active_path_heading_stale(self) -> bool:
        if self.active_path_replan_forward_axis is None or self.current_forward_axis is None:
            return False

        dot = float(np.clip(np.dot(self.active_path_replan_forward_axis, self.current_forward_axis), -1.0, 1.0))
        delta = math.acos(dot)
        threshold = float(self.get_parameter("replan_heading_delta_rad").value)
        return delta >= threshold

    def forward_gain(self, path):
        if len(path) < 2:
            return 0.0
        resolution = float(self.get_parameter("resolution_m").value)
        return float((path[-1][0] - path[0][0]) * resolution)

    def path_is_clear(self, path, grid, half_width_cells):
        if not path:
            return False
        for row, col in path:
            if not self.corridor_is_clear(grid, row, col, half_width_cells):
                return False
        return True

    def plan_path(self, grid: np.ndarray):
        resolution = float(self.get_parameter("resolution_m").value)
        clear_width = float(self.get_parameter("clear_width_m").value)
        half_width_cells = max(1, int(round((clear_width * 0.5) / resolution)))

        return self.forward_progress_path(grid, half_width_cells)

    def forward_progress_path(self, grid: np.ndarray, half_width_cells: int):
        rows, cols = grid.shape
        resolution = float(self.get_parameter("resolution_m").value)
        guidance_start = max(0.0, float(self.get_parameter("guidance_start_m").value))
        path_start_buffer = max(
            guidance_start,
            float(self.get_parameter("path_start_buffer_m").value),
        )
        max_step = max(1, int(self.get_parameter("max_lateral_step_cells").value))

        # Force the visible path to start under the current camera/person in the
        # frozen active-unit frame. Only the routing section begins a small
        # buffer distance ahead so the planner does not immediately reroute
        # around the camera's own blind/noisy footprint.
        center_col = cols // 2
        start_anchor_row = 0
        start_col = center_col
        cam_cell = self.camera_cell_in_active_unit()
        if cam_cell is not None:
            cam_row, cam_col, _, _ = cam_cell
            start_anchor_row = int(np.clip(cam_row, 0, rows - 1))
            start_col = int(np.clip(cam_col, half_width_cells, cols - half_width_cells - 1))

        buffer_cells = max(1, int(math.ceil(path_start_buffer / resolution)))
        guidance_cells = max(1, int(math.ceil(guidance_start / resolution)))
        start_row = min(rows - 1, start_anchor_row + buffer_cells)
        guidance_row = min(rows - 1, start_anchor_row + guidance_cells)

        planning_grid = grid.copy()

        # Never let the camera anchor/buffer area block the path. This is the
        # user's body/camera blind zone, not an obstacle to route around.
        clear_end = min(rows, start_row + 1)
        lo = max(0, start_col - half_width_cells)
        hi = min(cols, start_col + half_width_cells + 1)
        if start_anchor_row < clear_end:
            near = planning_grid[start_anchor_row:clear_end, lo:hi]
            near[near == 100] = 0
            near[near == 255] = 0

        free = self.compute_clearance_grid(planning_grid, half_width_cells)
        route_cell = self.find_nearby_clear_path_cell(free, start_row, start_col)
        if route_cell is None:
            # Still publish a short path directly under/ahead of the camera so
            # RViz and guidance have a sane camera-anchored reference instead of
            # disappearing completely.
            fallback = [(start_anchor_row, start_col)]
            if guidance_row != start_anchor_row:
                fallback.append((guidance_row, start_col))
            if start_row != guidance_row:
                fallback.append((start_row, start_col))
            return self.decimate_path(fallback)
        start_row, route_col = route_cell

        costs = np.full(cols, np.inf, dtype=np.float32)
        parents = np.full((rows, cols), -1, dtype=np.int16)
        costs[route_col] = 0.0

        best_row = start_row
        best_col = route_col
        prev_costs = costs

        for row in range(start_row + 1, rows):
            next_costs = np.full(cols, np.inf, dtype=np.float32)
            free_cols = np.flatnonzero(free[row])
            if free_cols.size == 0:
                break

            for col in free_cols:
                lo = max(0, col - max_step)
                hi = min(cols, col + max_step + 1)
                window = prev_costs[lo:hi]
                if not np.isfinite(window).any():
                    continue

                local_idx = int(np.nanargmin(window))
                parent_col = lo + local_idx
                lateral_cost = abs(col - parent_col) * 2.8
                camera_center_cost = abs(col - start_col) * 0.04
                next_costs[col] = window[local_idx] + lateral_cost + camera_center_cost
                parents[row, col] = parent_col

            if not np.isfinite(next_costs).any():
                break

            best_row = row
            best_col = int(np.nanargmin(next_costs))
            prev_costs = next_costs

        path = []
        row = best_row
        col = best_col
        while row >= start_row and col >= 0:
            path.append((row, col))
            parent_col = parents[row, col]
            row -= 1
            if row < start_row:
                break
            if parent_col >= 0:
                col = int(parent_col)
        path.append((start_row, route_col))
        path.reverse()

        anchors = []
        if bool(self.get_parameter("prepend_camera_anchor").value):
            anchors.append((start_anchor_row, start_col))
            if guidance_row > start_anchor_row:
                anchors.append((guidance_row, start_col))
        if path and anchors and path[0] != anchors[-1]:
            anchors.append(path[0])
        path = anchors + path[1:] if anchors and path else path
        return self.decimate_path(path)

    def find_nearby_clear_path_cell(self, free: np.ndarray, row: int, preferred_col: int):
        rows, cols = free.shape
        if row >= rows:
            return None
        max_radius = min(cols // 2, int(round(1.2 / float(self.get_parameter("resolution_m").value))))
        for rr in range(row, min(rows, row + 5)):
            if 0 <= preferred_col < cols and free[rr, preferred_col]:
                return rr, preferred_col
            for radius in range(1, max_radius + 1):
                for dc in (-radius, radius):
                    cc = preferred_col + dc
                    if 0 <= cc < cols and free[rr, cc]:
                        return rr, cc
        return None

    def camera_anchor_path(self, guidance_row: int, center_col: int):
        path = []
        if bool(self.get_parameter("prepend_camera_anchor").value):
            path.append((0, center_col))
            if guidance_row > 0:
                path.append((guidance_row, center_col))
        return self.decimate_path(path)

    def classify_guidance(self, path_cells) -> str:
        if len(path_cells) < 2:
            return "STOP!"

        resolution = float(self.get_parameter("resolution_m").value)
        start_row, start_col = path_cells[0]
        rows_m = np.array(
            [(row - start_row) * resolution for row, _ in path_cells],
            dtype=np.float32,
        )
        lateral_m = np.array(
            [(col - start_col) * resolution for _, col in path_cells],
            dtype=np.float32,
        )

        forward_gain = float(np.max(rows_m)) if rows_m.size else 0.0
        stop_distance = float(self.get_parameter("stop_path_distance_m").value)
        if forward_gain < stop_distance:
            return "STOP!"

        lookahead = float(self.get_parameter("guidance_first_turn_lookahead_m").value)
        turn_threshold = float(self.get_parameter("guidance_turn_lateral_threshold_m").value)
        ignore_near = float(self.get_parameter("guidance_ignore_near_m").value)

        actionable = np.flatnonzero(
            (rows_m >= ignore_near)
            & (rows_m <= lookahead)
            & (np.abs(lateral_m) >= turn_threshold)
        )
        if actionable.size == 0:
            return "FORWARD"

        first_idx = int(actionable[0])
        first_delta = float(lateral_m[first_idx])
        return self.guidance_side(first_delta)

    def classify_world_guidance(self) -> str:
        if (
            not self.active_path_world
            or self.current_floor_origin_odom is None
            or self.current_forward_axis is None
            or self.current_right_axis is None
        ):
            return "STOP!"

        # Evaluate guidance in the frozen active-unit frame. Using the live
        # camera heading here made a good fixed path look like it was behind the
        # camera whenever the user rotated slightly, causing false STOP.
        guide_forward = self.active_unit_forward_axis if self.active_unit_forward_axis is not None else self.current_forward_axis
        guide_right = self.active_unit_right_axis if self.active_unit_right_axis is not None else self.current_right_axis
        rel = np.array(self.active_path_world, dtype=np.float32) - self.current_floor_origin_odom
        forward_m = rel @ guide_forward
        lateral_m = rel @ guide_right

        stop_distance = float(self.get_parameter("stop_path_distance_m").value)
        if forward_m.size == 0 or float(np.max(forward_m)) < stop_distance:
            return "STOP!"

        lookahead = float(self.get_parameter("guidance_first_turn_lookahead_m").value)
        turn_threshold = float(self.get_parameter("guidance_turn_lateral_threshold_m").value)
        ignore_near = float(self.get_parameter("guidance_ignore_near_m").value)
        actionable = np.flatnonzero(
            (forward_m >= ignore_near)
            & (forward_m <= lookahead)
            & (np.abs(lateral_m) >= turn_threshold)
        )
        if actionable.size == 0:
            return "FORWARD"

        nearest_idx = int(actionable[np.argmin(forward_m[actionable])])
        return self.guidance_side(float(lateral_m[nearest_idx]))

    def guidance_side(self, lateral_delta_m: float) -> str:
        delta = lateral_delta_m
        if bool(self.get_parameter("invert_guidance_lr").value):
            delta = -delta

        # Grid lateral coordinates are published on -floor_left, so positive
        # lateral cells are camera-right and negative lateral cells are camera-left.
        return "RIGHT" if delta > 0.0 else "LEFT"

    def publish_guidance(self, text: str):
        text = self.stabilize_guidance(text)

        msg = String()
        msg.data = text
        self.guidance_pub.publish(msg)

        now = time.time()
        period = float(self.get_parameter("guidance_log_period_s").value)
        if text != self.last_guidance_text or (period > 0.0 and now - self.last_guidance_log >= period):
            self.get_logger().info(f"guidance: {text}")
            self.last_guidance_text = text
            self.last_guidance_log = now

    def stabilize_guidance(self, text: str) -> str:
        if not self.last_guidance_text:
            self.last_guidance_text = text
            self.pending_guidance_text = ""
            self.pending_guidance_count = 0
            return text

        if text == self.last_guidance_text:
            self.pending_guidance_text = ""
            self.pending_guidance_count = 0
            return self.last_guidance_text

        if text == self.pending_guidance_text:
            self.pending_guidance_count += 1
        else:
            self.pending_guidance_text = text
            self.pending_guidance_count = 1

        required = int(self.get_parameter("guidance_debounce_frames").value)
        if text == "STOP!":
            required = int(self.get_parameter("guidance_stop_debounce_frames").value)
        required = max(1, required)

        if self.pending_guidance_count >= required:
            self.last_guidance_text = text
            self.pending_guidance_text = ""
            self.pending_guidance_count = 0

        return self.last_guidance_text

    def furthest_straight_row(self, free: np.ndarray, start_row: int, center_col: int) -> int:
        furthest = start_row - 1
        for row in range(start_row, free.shape[0]):
            if not free[row, center_col]:
                break
            furthest = row
        return furthest

    def compute_clearance_grid(self, grid: np.ndarray, half_width_cells: int):
        occupied = (grid != 0).astype(np.uint8)
        kernel = np.ones((1, 2 * half_width_cells + 1), dtype=np.uint8)
        blocked = cv2.dilate(occupied, kernel, iterations=1) > 0
        clear = ~blocked
        clear[:, :half_width_cells] = False
        clear[:, grid.shape[1] - half_width_cells :] = False
        return clear

    def find_start_cell(self, grid: np.ndarray, half_width_cells: int):
        rows, cols = grid.shape
        center_col = cols // 2
        resolution = float(self.get_parameter("resolution_m").value)
        min_range = float(self.get_parameter("min_range_m").value)
        first_row = min(max(2, int(np.ceil(min_range / resolution)) + 1), rows - 1)
        last_row = min(rows - 1, first_row + int(round(0.6 / resolution)))
        max_radius = min(cols // 2, int(round(1.2 / resolution)))

        for start_row in range(first_row, last_row + 1):
            if self.corridor_is_clear(grid, start_row, center_col, half_width_cells):
                return (start_row, center_col)

            for radius in range(1, max_radius + 1):
                for dc in (-radius, radius):
                    col = center_col + dc
                    if self.corridor_is_clear(grid, start_row, col, half_width_cells):
                        return (start_row, col)

        return (first_row, center_col)

    def prepend_center_start(self, path, center_start):
        if not path:
            return path
        if path[0] != center_start:
            return [center_start] + path
        return path

    def decimate_path(self, path):
        if path:
            compact = [path[0]]
            for point in path[1:]:
                if point != compact[-1]:
                    compact.append(point)
            path = compact

        if len(path) <= 2:
            return path

        stride = max(1, int(self.get_parameter("path_stride_cells").value))
        out = [path[0]]
        last = path[0]
        last_dir = None

        for point in path[1:-1]:
            direction = (
                int(np.sign(point[0] - last[0])),
                int(np.sign(point[1] - last[1])),
            )
            row_gap = point[0] - out[-1][0]
            if direction != last_dir or row_gap >= stride:
                out.append(point)
                last_dir = direction
            last = point

        if out[-1] != path[-1]:
            out.append(path[-1])
        return out

    def corridor_is_clear(self, grid: np.ndarray, row: int, col: int, half_width_cells: int) -> bool:
        rows, cols = grid.shape
        if row < 0 or row >= rows or col < 0 or col >= cols:
            return False

        lo = col - half_width_cells
        hi = col + half_width_cells + 1
        if lo < 0 or hi > cols:
            return False

        return not np.any(grid[row, lo:hi] > 0)

    def furthest_clear_forward(self, grid: np.ndarray, start, half_width_cells: int):
        rows, _ = grid.shape
        row, col = start
        furthest = start

        for nr in range(row, rows):
            if not self.corridor_is_clear(grid, nr, col, half_width_cells):
                break
            furthest = (nr, col)

        return furthest

    def furthest_clear_lateral(self, grid: np.ndarray, start, half_width_cells: int, direction: int):
        _, cols = grid.shape
        row, col = start
        furthest = start

        nc = col
        while True:
            nc += direction
            if nc < 0 or nc >= cols:
                break
            if not self.corridor_is_clear(grid, row, nc, half_width_cells):
                break
            furthest = (row, nc)

        return furthest

    def make_directing_path(self, start, straight_goal, goal):
        stride = max(1, int(self.get_parameter("path_stride_cells").value))
        path = []
        start_row, start_col = start
        straight_row, straight_col = straight_goal
        goal_row, goal_col = goal

        for row in range(start_row, straight_row + 1, stride):
            path.append((row, start_col))
        if not path or path[-1] != straight_goal:
            path.append(straight_goal)

        if goal_col != straight_col:
            step = 1 if goal_col > straight_col else -1
            for col in range(straight_col + step, goal_col + step, step * stride):
                path.append((goal_row, col))
            if path[-1] != goal:
                path.append(goal)

        return path

    def publish_grid(self, msg: PointCloud2, grid: np.ndarray, basis):
        resolution = float(self.get_parameter("resolution_m").value)
        grid_width_m = float(self.get_parameter("grid_width_m").value)
        frame = str(self.get_parameter("grid_frame").value)

        rows, cols = grid.shape

        occ = OccupancyGrid()
        occ.header.stamp = msg.header.stamp
        occ.header.frame_id = frame

        occ.info.resolution = resolution
        occ.info.width = rows
        occ.info.height = cols
        if basis is None or self.last_plane is None:
            floor_forward = np.array([1.0, 0.0, 0.0], dtype=np.float32)
            floor_left = np.array([0.0, 1.0, 0.0], dtype=np.float32)
            floor_normal = np.array([0.0, 0.0, 1.0], dtype=np.float32)
            floor_origin = np.zeros(3, dtype=np.float32)
        else:
            floor_forward, floor_left, floor_normal = basis
            _, d = self.last_plane
            floor_origin = -d * floor_normal

        map_y_axis = -floor_left
        origin = floor_origin + map_y_axis * (-grid_width_m / 2.0)
        quat = self.rotation_to_quaternion(floor_forward, map_y_axis, floor_normal)

        occ.info.origin.position.x = float(origin[0])
        occ.info.origin.position.y = float(origin[1])
        occ.info.origin.position.z = float(origin[2])
        occ.info.origin.orientation.x = quat[0]
        occ.info.origin.orientation.y = quat[1]
        occ.info.origin.orientation.z = quat[2]
        occ.info.origin.orientation.w = quat[3]

        # OccupancyGrid x = forward and y = lateral, matching /navivest/path.
        rviz_grid = np.full_like(grid, -1, dtype=np.int8)
        rviz_grid[grid == 0] = 0
        rviz_grid[grid == 100] = 100
        occ.data = rviz_grid.T.flatten().tolist()

        self.grid_pub.publish(occ)

    def publish_path(self, msg: PointCloud2, path_cells, basis, origin):
        if not path_cells or basis is None:
            return

        resolution = float(self.get_parameter("resolution_m").value)
        grid_width_m = float(self.get_parameter("grid_width_m").value)
        frame = str(self.get_parameter("grid_frame").value)
        floor_forward, floor_left, floor_normal = basis
        map_y_axis = -floor_left

        path = Path()
        path.header.stamp = msg.header.stamp
        path.header.frame_id = frame

        for r, c in path_cells:
            forward_m = r * resolution
            side_m = c * resolution - grid_width_m / 2.0
            point = origin + floor_forward * forward_m + map_y_axis * side_m + floor_normal * 0.04

            pose = PoseStamped()
            pose.header = path.header
            pose.pose.position.x = float(point[0])
            pose.pose.position.y = float(point[1])
            pose.pose.position.z = float(point[2])
            pose.pose.orientation.w = 1.0
            path.poses.append(pose)

        self.path_pub.publish(path)

    def publish_world_path(self, msg: PointCloud2):
        if not self.active_path_world:
            return

        frame = str(self.get_parameter("odom_frame").value)
        path = Path()
        path.header.stamp = msg.header.stamp
        path.header.frame_id = frame

        for point in self.active_path_world:
            pose = PoseStamped()
            pose.header = path.header
            pose.pose.position.x = float(point[0])
            pose.pose.position.y = float(point[1])
            pose.pose.position.z = float(point[2]) + 0.04
            pose.pose.orientation.w = 1.0
            path.poses.append(pose)

        self.path_pub.publish(path)

    def publish_rolling_grid(self, msg: PointCloud2):
        if (
            self.rolling_display_grid is None
            or self.memory_origin_odom is None
            or self.memory_forward_axis is None
            or self.memory_right_axis is None
            or self.memory_normal_axis is None
            or self.memory_center_segment is None
        ):
            return

        resolution = float(self.get_parameter("resolution_m").value)
        grid_width_m = float(self.get_parameter("grid_width_m").value)
        segment_len = float(self.get_parameter("grid_forward_m").value)
        frame = str(self.get_parameter("odom_frame").value)
        forward_count = max(3, int(self.get_parameter("memory_forward_grid_count").value))
        lateral_count = max(3, int(self.get_parameter("memory_lateral_grid_count").value))
        if forward_count % 2 == 0:
            forward_count += 1
        if lateral_count % 2 == 0:
            lateral_count += 1
        first_forward_segment = self.memory_center_segment[0] - forward_count // 2
        first_lateral_segment = self.memory_center_segment[1] - lateral_count // 2

        origin = (
            self.memory_origin_odom
            + self.memory_forward_axis * (first_forward_segment * segment_len)
            + self.memory_right_axis * (first_lateral_segment * grid_width_m - grid_width_m / 2.0)
        )
        quat = self.rotation_to_quaternion(
            self.memory_forward_axis,
            self.memory_right_axis,
            self.memory_normal_axis,
        )

        occ = OccupancyGrid()
        occ.header.stamp = msg.header.stamp
        occ.header.frame_id = frame
        occ.info.resolution = resolution
        occ.info.width = self.rolling_display_grid.shape[0]
        occ.info.height = self.rolling_display_grid.shape[1]
        occ.info.origin.position.x = float(origin[0])
        occ.info.origin.position.y = float(origin[1])
        occ.info.origin.position.z = float(origin[2])
        occ.info.origin.orientation.x = quat[0]
        occ.info.origin.orientation.y = quat[1]
        occ.info.origin.orientation.z = quat[2]
        occ.info.origin.orientation.w = quat[3]

        rviz_grid = np.full_like(self.rolling_display_grid, -1, dtype=np.int8)
        rviz_grid[self.rolling_display_grid == 0] = 0
        rviz_grid[self.rolling_display_grid == 100] = 100
        occ.data = rviz_grid.T.flatten().tolist()
        self.grid_pub.publish(occ)

    def rotation_to_quaternion(self, x_axis: np.ndarray, y_axis: np.ndarray, z_axis: np.ndarray):
        rot = np.eye(3, dtype=np.float64)
        rot[:, 0] = x_axis / max(np.linalg.norm(x_axis), 1e-6)
        rot[:, 1] = y_axis / max(np.linalg.norm(y_axis), 1e-6)
        rot[:, 2] = z_axis / max(np.linalg.norm(z_axis), 1e-6)

        if np.linalg.det(rot) < 0:
            rot[:, 2] *= -1.0

        trace = float(np.trace(rot))
        if trace > 0.0:
            s = math.sqrt(trace + 1.0) * 2.0
            qw = 0.25 * s
            qx = (rot[2, 1] - rot[1, 2]) / s
            qy = (rot[0, 2] - rot[2, 0]) / s
            qz = (rot[1, 0] - rot[0, 1]) / s
        elif rot[0, 0] > rot[1, 1] and rot[0, 0] > rot[2, 2]:
            s = math.sqrt(1.0 + rot[0, 0] - rot[1, 1] - rot[2, 2]) * 2.0
            qw = (rot[2, 1] - rot[1, 2]) / s
            qx = 0.25 * s
            qy = (rot[0, 1] + rot[1, 0]) / s
            qz = (rot[0, 2] + rot[2, 0]) / s
        elif rot[1, 1] > rot[2, 2]:
            s = math.sqrt(1.0 + rot[1, 1] - rot[0, 0] - rot[2, 2]) * 2.0
            qw = (rot[0, 2] - rot[2, 0]) / s
            qx = (rot[0, 1] + rot[1, 0]) / s
            qy = 0.25 * s
            qz = (rot[1, 2] + rot[2, 1]) / s
        else:
            s = math.sqrt(1.0 + rot[2, 2] - rot[0, 0] - rot[1, 1]) * 2.0
            qw = (rot[1, 0] - rot[0, 1]) / s
            qx = (rot[0, 2] + rot[2, 0]) / s
            qy = (rot[1, 2] + rot[2, 1]) / s
            qz = 0.25 * s

        norm = math.sqrt(qx * qx + qy * qy + qz * qz + qw * qw)
        return (
            float(qx / norm),
            float(qy / norm),
            float(qz / norm),
            float(qw / norm),
        )

    def publish_debug(self, msg: PointCloud2, raw: np.ndarray, inflated: np.ndarray, path_cells):
        scale = int(self.get_parameter("debug_scale").value)

        img = np.zeros((raw.shape[0], raw.shape[1], 3), dtype=np.uint8)
        img[:] = (240, 240, 240)

        img[inflated > 0] = (0, 0, 0)
        img[raw > 0] = (0, 0, 255)

        for r, c in path_cells:
            if 0 <= r < img.shape[0] and 0 <= c < img.shape[1]:
                img[r, c] = (0, 255, 0)

        # Put forward direction upward in debug image.
        img = np.flipud(img)
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)

        out = Image()
        out.header.stamp = self.get_clock().now().to_msg()
        out.header.frame_id = str(self.get_parameter("grid_frame").value)
        out.height = img.shape[0]
        out.width = img.shape[1]
        out.encoding = "bgr8"
        out.is_bigendian = False
        out.step = img.shape[1] * 3
        out.data = img.tobytes()

        self.debug_pub.publish(out)

    def throttled_warn(self, text: str):
        now = time.time()
        if now - self.last_log > 1.5:
            self.get_logger().warn(text)
            self.last_log = now

    def log_stats(self, elapsed_s: float, path_len: int):
        self.frame_count += 1
        now = time.time()
        period = float(self.get_parameter("stats_period_s").value)
        if period <= 0.0 or now - self.last_stats_log < period:
            return

        hz = self.frame_count / max(now - self.last_stats_log, 1e-6)
        self.get_logger().info(
            f"topdown {hz:.1f} hz, frame {elapsed_s * 1000.0:.1f} ms, "
            f"path_cells={path_len}"
        )
        self.frame_count = 0
        self.last_stats_log = now


def main(args=None):
    rclpy.init(args=args)
    node = ZedTopdownAStar()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
