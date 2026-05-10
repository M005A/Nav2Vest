#!/usr/bin/env python3

import math
import time
from typing import Optional, Tuple

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import PointCloud2, Image
from sensor_msgs_py import point_cloud2
from nav_msgs.msg import OccupancyGrid, Path
from geometry_msgs.msg import PoseStamped


class ZedTopdownAStar(Node):
    def __init__(self):
        super().__init__("zed_topdown_astar")

        self.declare_parameter("cloud_topic", "/zed/zed_node/point_cloud/cloud_registered")
        self.declare_parameter("grid_frame", "zed_left_camera_frame")

        self.declare_parameter("grid_width_m", 5.0)
        self.declare_parameter("grid_forward_m", 5.0)
        self.declare_parameter("resolution_m", 0.05)

        self.declare_parameter("min_range_m", 0.55)
        self.declare_parameter("guidance_start_m", 0.10)
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

        self.grid_pub = self.create_publisher(OccupancyGrid, "/navivest/occupancy_grid", 10)
        self.path_pub = self.create_publisher(Path, "/navivest/path", 10)
        self.debug_pub = self.create_publisher(Image, "/navivest/debug_topdown", 10)

        self.last_plane: Optional[Tuple[np.ndarray, float]] = None
        self.display_obstacle_memory: Optional[np.ndarray] = None
        self.planning_obstacle_memory: Optional[np.ndarray] = None
        self.free_space_memory: Optional[np.ndarray] = None
        self.last_path_cells = []
        self.last_process_time = 0.0
        self.last_log = 0.0
        self.last_stats_log = time.time()
        self.frame_count = 0

        self.get_logger().info(f"Subscribed to {self.cloud_topic}")

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
            candidate_path = self.plan_path(planning_grid)
            path_cells = self.stabilize_path(candidate_path, planning_grid)

            self.publish_grid(msg, display_grid, basis)
            self.publish_path(msg, path_cells, basis, origin)
            if bool(self.get_parameter("publish_debug").value):
                self.publish_debug(msg, grid, display_grid, path_cells)
            self.log_stats(time.perf_counter() - now, len(path_cells))

        except Exception as e:
            self.get_logger().error(f"cloud_cb failed: {e}")

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
        center_col = cols // 2
        resolution = float(self.get_parameter("resolution_m").value)
        min_range = float(self.get_parameter("min_range_m").value)
        guidance_start = max(0.0, float(self.get_parameter("guidance_start_m").value))
        route_start = max(min_range, guidance_start)
        guidance_row = min(max(1, int(np.ceil(guidance_start / resolution))), rows - 1)
        start_row = min(max(2, int(np.ceil(route_start / resolution)) + 1), rows - 1)
        max_step = max(1, int(self.get_parameter("max_lateral_step_cells").value))

        free = self.compute_clearance_grid(grid, half_width_cells)
        if not free[start_row, center_col]:
            return self.camera_anchor_path(guidance_row, center_col)

        straight_row = self.furthest_straight_row(free, start_row, center_col)

        costs = np.full(cols, np.inf, dtype=np.float32)
        parents = np.full((rows, cols), -1, dtype=np.int16)

        costs[center_col] = 0.0

        best_row = start_row
        best_col = int(np.nanargmin(costs))
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
                center_cost = abs(col - center_col) * 0.06
                next_costs[col] = window[local_idx] + lateral_cost + center_cost
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
        path.append((start_row, center_col))
        path.reverse()

        reroute_min_gain = float(self.get_parameter("reroute_min_forward_gain_m").value)
        reroute_min_gain_cells = max(0, int(round(reroute_min_gain / resolution)))
        if straight_row >= start_row and best_row <= straight_row + reroute_min_gain_cells:
            path = [(row, center_col) for row in range(start_row, straight_row + 1)]

        if bool(self.get_parameter("prepend_camera_anchor").value):
            if guidance_row < start_row:
                path.insert(0, (guidance_row, center_col))
            path.insert(0, (0, center_col))
        return self.decimate_path(path)

    def camera_anchor_path(self, guidance_row: int, center_col: int):
        path = []
        if bool(self.get_parameter("prepend_camera_anchor").value):
            path.append((0, center_col))
            if guidance_row > 0:
                path.append((guidance_row, center_col))
        return self.decimate_path(path)

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
        occ.header.stamp = self.get_clock().now().to_msg()
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
        path.header.stamp = self.get_clock().now().to_msg()
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
