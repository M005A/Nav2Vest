#!/usr/bin/env python3
"""NaviVest public booth demo UI.

A small NiceGUI web dashboard for prerecorded ZED SVO demos.
The intended booth flow is simple:

    1. Select a prerecorded .svo/.svo2 file.
    2. Press Play Demo.
    3. The configured ROS launch command starts SVO playback.
    4. Visitors watch the route/cue display and feel the haptic feedback.

Run:
    python3 navivest_demo_gui.py --svo-dir ~/navivest_svos

Optional backend mirror:
    python3 navivest_demo_gui.py --data demo_state.json

Optional launch override:
    python3 navivest_demo_gui.py \
      --launch-command 'ros2 launch navivest_bringup navivest_svo_guidance.launch.py svo_path:={svo} rviz:=true audio:=true'
"""

from __future__ import annotations

import argparse
import json
import math
import os
import shlex
import signal
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from nicegui import app, ui

os.environ.setdefault("FASTDDS_BUILTIN_TRANSPORTS", "UDPv4")

DEFAULT_LAUNCH_COMMAND = (
    "export FASTDDS_BUILTIN_TRANSPORTS=UDPv4 && "
    "source /opt/ros/jazzy/setup.bash && "
    "source /home/macho/navivest_ws/install/setup.bash && "
    "ros2 launch navivest_bringup navivest_full_svo.launch.py "
    "svo_path:={svo} rviz:=true audio:=true"
)

BG = "#fff8ec"
CARD = "#ffffff"
TEXT = "#18223a"
MUTED = "#64748b"
BORDER = "#f1dec1"
ACCENT = "#ff8a3d"
ACCENT_DARK = "#cc5f1e"
TEAL = "#1ca7a8"
GREEN = "#2fb977"
YELLOW = "#f4b740"
RED = "#e5484d"
PURPLE = "#8a63d2"
PATH_GREEN = "#1aa884"
OBSTACLE = "#f06a6a"


@dataclass
class DemoPreset:
    name: str
    duration_s: int
    description: str
    obstacles: List[Dict[str, Any]]
    planned_path: List[Dict[str, float]]
    cue_schedule: List[tuple[int, str, str]]


PRESETS = [
    DemoPreset(
        name="Chair in Walkway",
        duration_s=70,
        description="A chair blocks part of the walking path, so NaviVest plans a gentle route around it.",
        obstacles=[{"x": 0.8, "y": 2.2, "type": "chair"}, {"x": 1.15, "y": 2.55, "type": "blocked"}],
        planned_path=[
            {"x": 0.0, "y": 0.0}, {"x": -0.08, "y": 0.8}, {"x": -0.36, "y": 1.7},
            {"x": -0.48, "y": 2.7}, {"x": -0.20, "y": 3.8}, {"x": 0.0, "y": 4.8},
        ],
        cue_schedule=[
            (0, "FORWARD", "Path is clear ahead."),
            (10, "BEAR LEFT", "Shift slightly left to stay on the safe path."),
            (22, "LEFT IN 0.5 METERS", "Prepare to move left soon."),
            (34, "FORWARD", "Continue forward through the clear space."),
            (53, "BEAR RIGHT", "Return gently toward the center of the safe path."),
        ],
    ),
    DemoPreset(
        name="Person Crossing",
        duration_s=64,
        description="A moving person crosses the path, causing a brief pause and safe recovery.",
        obstacles=[{"x": 0.0, "y": 1.9, "type": "person"}],
        planned_path=[
            {"x": 0.0, "y": 0.0}, {"x": 0.0, "y": 0.9}, {"x": 0.1, "y": 1.4},
            {"x": 0.42, "y": 2.3}, {"x": 0.28, "y": 3.4}, {"x": 0.0, "y": 4.7},
        ],
        cue_schedule=[
            (0, "FORWARD", "Path is clear ahead."),
            (15, "STOP", "Obstacle detected. Pause."),
            (25, "PATH CLEAR", "The path is clear again."),
            (31, "RIGHT NOW", "Move right now to stay on the safe route."),
            (45, "FORWARD", "Continue forward."),
        ],
    ),
    DemoPreset(
        name="Obstacle on Left",
        duration_s=58,
        description="An obstacle appears on the left, so the guidance shifts right and then recenters.",
        obstacles=[{"x": -0.95, "y": 2.0, "type": "box"}, {"x": -0.55, "y": 2.6, "type": "blocked"}],
        planned_path=[
            {"x": 0.0, "y": 0.0}, {"x": 0.12, "y": 0.9}, {"x": 0.45, "y": 1.8},
            {"x": 0.55, "y": 2.7}, {"x": 0.22, "y": 3.7}, {"x": 0.0, "y": 4.8},
        ],
        cue_schedule=[
            (0, "FORWARD", "Path is clear ahead."),
            (12, "RIGHT IN 0.5 METERS", "Prepare to turn right soon."),
            (22, "RIGHT NOW", "Move right now to stay on the safe route."),
            (35, "BEAR LEFT", "Shift slightly left to return to center."),
            (48, "FORWARD", "Continue forward."),
        ],
    ),
    DemoPreset(
        name="Narrow Hallway",
        duration_s=75,
        description="The safe route stays centered between blocked regions in a narrow hallway.",
        obstacles=[{"x": -1.15, "y": 1.5, "type": "wall"}, {"x": 1.15, "y": 1.7, "type": "wall"}],
        planned_path=[
            {"x": 0.0, "y": 0.0}, {"x": 0.0, "y": 1.0}, {"x": -0.05, "y": 2.0},
            {"x": 0.03, "y": 3.0}, {"x": 0.0, "y": 4.8},
        ],
        cue_schedule=[
            (0, "FORWARD", "Path is clear ahead."),
            (18, "BEAR LEFT", "Shift slightly left to stay centered."),
            (31, "FORWARD", "Continue forward through the clear space."),
            (44, "BEAR RIGHT", "Shift slightly right to stay centered."),
            (60, "FORWARD", "Continue forward."),
        ],
    ),
]

CUE_META = {
    "READY": ("●", TEAL, "Ready for prerecorded SVO playback."),
    "FORWARD": ("↑", GREEN, "Path is clear ahead."),
    "STOP": ("■", RED, "Obstacle detected. Pause."),
    "STOP!": ("■", RED, "Obstacle detected. Pause."),
    "WAIT": ("■", RED, "Obstacle detected. Pause."),
    "PATH CLEAR": ("✓", TEAL, "The path is clear again."),
    "BEAR LEFT": ("↖", YELLOW, "Shift slightly left to stay on the safe path."),
    "BEAR RIGHT": ("↗", YELLOW, "Shift slightly right to stay on the safe path."),
    "LEFT": ("⬅", ACCENT, "Move left to stay on the safe route."),
    "RIGHT": ("➡", ACCENT, "Move right to stay on the safe route."),
    "LEFT NOW": ("⬅", ACCENT, "Move left now."),
    "RIGHT NOW": ("➡", ACCENT, "Move right now."),
    "LEFT IN 0.5 METERS": ("↙", PURPLE, "Prepare to move left soon."),
    "RIGHT IN 0.5 METERS": ("↘", PURPLE, "Prepare to move right soon."),
}


def fmt_time(seconds: int) -> str:
    seconds = max(0, int(seconds))
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def parse_time(value: Any) -> int:
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str) and ":" in value:
        mm, ss = value.split(":", 1)
        return int(mm) * 60 + int(ss)
    return 0


def cue_for_time(preset: DemoPreset, seconds: int) -> tuple[str, str]:
    cue, text = preset.cue_schedule[0][1], preset.cue_schedule[0][2]
    for t, candidate, explanation in preset.cue_schedule:
        if seconds >= t:
            cue, text = candidate, explanation
        else:
            break
    return cue, text


def haptic_for_cue(cue: str) -> Dict[str, bool]:
    cue = cue.upper()
    stop = cue in {"STOP", "STOP!", "WAIT"}
    left = "LEFT" in cue
    right = "RIGHT" in cue
    forward = cue in {"FORWARD", "PATH CLEAR"}
    return {
        "left_shoulder": left or forward or stop,
        "right_shoulder": right or forward or stop,
        "left_back": left or stop,
        "right_back": right or stop,
    }


class DemoController:
    def __init__(self, svo_dir: Path, data_path: Optional[Path], launch_command: str):
        self.svo_dir = svo_dir.expanduser()
        self.data_path = data_path.expanduser() if data_path else None
        self.launch_command = launch_command
        self.selected_svo: Optional[Path] = None
        self.manual_svo_text = ""
        self.process: Optional[subprocess.Popen[str]] = None
        self.started_at: Optional[float] = None
        self.elapsed_s = 0.0
        self.external_state: Dict[str, Any] = {}
        self.external_mtime = 0.0
        self.preset_index = 0
        self.status = "Select a prerecorded SVO file, then press Play Demo."
        self.ros_lock = threading.Lock()
        self.ros_grid: Optional[Dict[str, Any]] = None
        self.ros_path: List[Tuple[float, float]] = []
        self.ros_status = "ROS top-down view waiting for /navivest/occupancy_grid."
        self.launch_log: List[str] = []
        self.ros_guidance = ""
        self.ros_audio_cue = ""
        self.ros_guidance_time = 0.0
        self.ros_audio_time = 0.0

    @property
    def is_running(self) -> bool:
        return self.process is not None and self.process.poll() is None

    def set_selected_svo(self, value: str) -> None:
        text = str(value or "").strip()
        self.manual_svo_text = text
        self.selected_svo = Path(text).expanduser() if text else None
        if text:
            self.status = "SVO path selected. Press Play Demo to launch."
        else:
            self.status = "Select or enter a prerecorded SVO file."

    def scan_svos(self) -> List[str]:
        try:
            files = sorted([*self.svo_dir.glob("*.svo"), *self.svo_dir.glob("*.svo2")])
        except OSError:
            files = []
        return [str(p) for p in files]

    def load_external_state(self) -> None:
        if not self.data_path:
            return
        try:
            stat = self.data_path.stat()
        except OSError:
            return
        if stat.st_mtime <= self.external_mtime:
            return
        try:
            self.external_state = json.loads(self.data_path.read_text())
            self.external_mtime = stat.st_mtime
        except Exception as exc:
            self.status = f"Could not read demo state JSON: {exc}"

    def play(self) -> None:
        if self.is_running:
            self.status = "Demo is already running."
            return
        if self.selected_svo is None and self.manual_svo_text.strip():
            self.set_selected_svo(self.manual_svo_text)
        if self.selected_svo is None:
            self.status = "Select or enter a prerecorded .svo or .svo2 file first."
            ui.notify(self.status, type="warning")
            return
        if not self.selected_svo.exists():
            self.status = f"SVO file not found: {self.selected_svo}"
            ui.notify(self.status, type="negative")
            return

        quoted_svo = shlex.quote(str(self.selected_svo))
        command = self.launch_command.format(svo=quoted_svo)
        try:
            self.process = subprocess.Popen(
                command,
                shell=True,
                executable="/bin/bash",
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                preexec_fn=os.setsid if hasattr(os, "setsid") else None,
                text=True,
                env={**os.environ, "FASTDDS_BUILTIN_TRANSPORTS": "UDPv4"},
            )
            threading.Thread(target=self.read_launch_output, args=(self.process,), daemon=True).start()
            self.started_at = time.time()
            self.elapsed_s = 0.0
            self.status = "Playing prerecorded SVO demo."
            ui.notify("SVO demo launched", type="positive")
        except Exception as exc:
            self.process = None
            self.started_at = None
            self.status = f"Failed to launch demo: {exc}"
            ui.notify(self.status, type="negative")

    def read_launch_output(self, process: subprocess.Popen[str]) -> None:
        if process.stdout is None:
            return
        for line in process.stdout:
            line = line.rstrip()
            if not line:
                continue
            with self.ros_lock:
                self.launch_log.append(line)
                self.launch_log = self.launch_log[-12:]
            if "Subscribed to /zed/zed_node/point_cloud/cloud_registered" in line:
                self.ros_status = "Planner running; waiting for top-down grid."
            elif "/navivest/occupancy_grid" in line:
                self.ros_status = "Waiting for occupancy grid messages."

    def stop(self) -> None:
        if not self.process:
            self.status = "Demo is not running."
            return
        try:
            if self.is_running:
                if hasattr(os, "killpg"):
                    os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                else:
                    self.process.terminate()
                try:
                    self.process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    if hasattr(os, "killpg"):
                        os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
                    else:
                        self.process.kill()
            self.status = "Demo stopped."
            ui.notify("SVO demo stopped", type="info")
        finally:
            self.process = None
            self.started_at = None

    def tick(self) -> None:
        self.load_external_state()
        if self.is_running and self.started_at is not None:
            self.elapsed_s = time.time() - self.started_at
        elif self.process is not None and not self.is_running:
            self.status = "Demo process ended."
            self.process = None
            self.started_at = None

    def current_state(self) -> Dict[str, Any]:
        preset = PRESETS[self.preset_index]
        cue, explanation = cue_for_time(preset, int(self.elapsed_s))
        live_guidance, live_audio, live_age = self.ros_cue_snapshot()
        haptic_cue = cue
        if live_audio:
            cue = live_audio.upper()
            haptic_cue = cue
            explanation = "Current direction from /navivest/audio_cue."
        elif live_guidance:
            cue = live_guidance.upper()
            haptic_cue = cue
            explanation = "Waiting for the next audio cue; showing immediate /navivest/guidance."
        duration = preset.duration_s
        progress = min(1.0, self.elapsed_s / max(1, duration))
        state: Dict[str, Any] = {
            "demoMode": "SVO Playback",
            "scenarioName": self.selected_svo.name if self.selected_svo else preset.name,
            "isPlaying": self.is_running,
            "timestamp": fmt_time(int(self.elapsed_s)),
            "duration": fmt_time(duration),
            "progress": progress,
            "svoLoaded": self.selected_svo is not None,
            "depthPlaybackActive": self.is_running,
            "plannerActive": self.is_running,
            "audioCue": cue if self.is_running or live_audio or live_guidance else "READY",
            "plainEnglishCue": explanation if self.is_running or live_audio or live_guidance else "Select an SVO file and press Play Demo.",
            "immediateGuidance": live_guidance,
            "audioCueAge": live_age,
            "obstacles": preset.obstacles,
            "plannedPath": preset.planned_path,
            "hapticZones": haptic_for_cue(haptic_cue if self.is_running or live_audio or live_guidance else ""),
            "description": preset.description,
        }
        if self.external_state:
            state.update(self.external_state)
            if "progress" not in self.external_state:
                dur = max(1, parse_time(state.get("duration")))
                state["progress"] = min(1.0, parse_time(state.get("timestamp")) / dur)
        return state

    def set_ros_grid(self, msg: Any) -> None:
        with self.ros_lock:
            self.ros_grid = {
                "width": int(msg.info.width),
                "height": int(msg.info.height),
                "resolution": float(msg.info.resolution),
                "origin_x": float(msg.info.origin.position.x),
                "origin_y": float(msg.info.origin.position.y),
                "qx": float(msg.info.origin.orientation.x),
                "qy": float(msg.info.origin.orientation.y),
                "qz": float(msg.info.origin.orientation.z),
                "qw": float(msg.info.origin.orientation.w),
                "data": list(msg.data),
            }
            self.ros_status = "Live ROS occupancy grid and path."

    def set_ros_path(self, msg: Any) -> None:
        points = [(float(p.pose.position.x), float(p.pose.position.y)) for p in msg.poses]
        with self.ros_lock:
            self.ros_path = points

    def set_ros_guidance(self, text: str) -> None:
        with self.ros_lock:
            self.ros_guidance = text.strip()
            self.ros_guidance_time = time.time()

    def set_ros_audio(self, text: str) -> None:
        with self.ros_lock:
            self.ros_audio_cue = text.strip()
            self.ros_audio_time = time.time()

    def ros_cue_snapshot(self) -> Tuple[str, str, float]:
        now = time.time()
        with self.ros_lock:
            guidance = self.ros_guidance
            audio = self.ros_audio_cue
            audio_age = now - self.ros_audio_time if self.ros_audio_time > 0.0 else math.inf
            guidance_age = now - self.ros_guidance_time if self.ros_guidance_time > 0.0 else math.inf
        # Audio is intentionally sparse; keep the last cue visible a little
        # longer than the immediate guidance.
        if audio_age > 8.0:
            audio = ""
        if guidance_age > 2.0:
            guidance = ""
        return guidance, audio, min(audio_age, guidance_age)

    def ros_snapshot(self) -> Tuple[Optional[Dict[str, Any]], List[Tuple[float, float]], str]:
        with self.ros_lock:
            grid = dict(self.ros_grid) if self.ros_grid is not None else None
            path = list(self.ros_path)
            status = self.ros_status
        return grid, path, status

    def recent_launch_log(self) -> str:
        with self.ros_lock:
            return "\n".join(self.launch_log[-8:])


controller: DemoController
svo_select: Any
manual_path: Any
launch_btn: Any
stop_btn: Any
main_view: Any


def card() -> ui.card:
    return ui.card().classes("rounded-3xl shadow-sm border border-orange-100 bg-white min-w-0 max-w-full overflow-hidden")


def status_chip(label: str, value: str, ok: bool = True) -> None:
    color = "green" if ok else "orange"
    with ui.row().classes("items-center justify-between w-full py-1"):
        with ui.row().classes("items-center gap-2"):
            ui.icon("fiber_manual_record", color=color).classes("text-xs")
            ui.label(label).classes("font-semibold text-slate-800")
        ui.badge(value, color=color).classes("px-3 py-1")


def start_ros_monitor() -> None:
    try:
        import rclpy
        from nav_msgs.msg import OccupancyGrid, Path as RosPath
        from rclpy.node import Node
        from std_msgs.msg import String
    except Exception as exc:
        controller.ros_status = f"ROS monitor unavailable: {exc}"
        return

    class TopdownMonitor(Node):
        def __init__(self):
            super().__init__("navivest_demo_gui_topdown_monitor")
            self.create_subscription(OccupancyGrid, "/navivest/occupancy_grid", self.grid_cb, 10)
            self.create_subscription(RosPath, "/navivest/path", self.path_cb, 10)
            self.create_subscription(String, "/navivest/guidance", self.guidance_cb, 10)
            self.create_subscription(String, "/navivest/audio_cue", self.audio_cb, 10)

        def grid_cb(self, msg):
            controller.set_ros_grid(msg)

        def path_cb(self, msg):
            controller.set_ros_path(msg)

        def guidance_cb(self, msg):
            controller.set_ros_guidance(msg.data)

        def audio_cb(self, msg):
            controller.set_ros_audio(msg.data)

    def spin() -> None:
        try:
            rclpy.init(args=None)
            node = TopdownMonitor()
            rclpy.spin(node)
        except Exception as exc:
            controller.ros_status = f"ROS monitor stopped: {exc}"
        finally:
            try:
                if rclpy.ok():
                    rclpy.shutdown()
            except Exception:
                pass

    threading.Thread(target=spin, daemon=True).start()


def guidance_card(state: Dict[str, Any]) -> None:
    cue = str(state.get("audioCue", "READY")).upper()
    arrow, color, default_text = CUE_META.get(cue, ("●", TEAL, "Ready for prerecorded SVO playback."))
    explanation = state.get("plainEnglishCue", default_text)
    immediate = str(state.get("immediateGuidance", "") or "")
    with card().classes("p-6"):
        ui.label("Current Guidance").classes("text-sm font-bold text-slate-500 uppercase tracking-wide")
        with ui.row().classes("items-center gap-5 mt-4"):
            ui.html(f'<div class="pulse-dot" style="background:{color}">{arrow}</div>')
            with ui.column().classes("gap-1"):
                ui.label(cue).classes("text-5xl font-black text-slate-900")
                ui.label(str(explanation)).classes("text-lg text-slate-600")
                if immediate:
                    ui.badge(f"Immediate: {immediate}", color="blue").classes("mt-2")
        ui.separator().classes("my-5")
        ui.label("Audio cue and haptic pattern update from the live ROS guidance topics when the demo is running.").classes(
            "text-sm font-semibold text-orange-700"
        )


def yaw_from_quaternion(qx: float, qy: float, qz: float, qw: float) -> float:
    return math.atan2(2.0 * (qw * qz + qx * qy), 1.0 - 2.0 * (qy * qy + qz * qz))


def world_to_grid_px(grid: Dict[str, Any], x: float, y: float, sx: float, sy: float, ox: float, oy: float) -> Tuple[float, float]:
    yaw = yaw_from_quaternion(grid["qx"], grid["qy"], grid["qz"], grid["qw"])
    dx = x - grid["origin_x"]
    dy = y - grid["origin_y"]
    c = math.cos(-yaw)
    s = math.sin(-yaw)
    gx = (c * dx - s * dy) / max(1e-6, grid["resolution"])
    gy = (s * dx + c * dy) / max(1e-6, grid["resolution"])
    return ox + gx * sx, oy + (grid["height"] - gy) * sy


def ros_topdown_svg() -> Optional[str]:
    grid, path, status = controller.ros_snapshot()
    if grid is None:
        return None

    width, height = 520, 440
    mx, my, mw, mh = 32, 38, 456, 350
    cols = max(1, int(grid["width"]))
    rows = max(1, int(grid["height"]))
    data = grid["data"]
    stride = max(1, int(math.ceil(max(cols, rows) / 135)))
    yaw = yaw_from_quaternion(grid["qx"], grid["qy"], grid["qz"], grid["qw"])
    yaw_cos = math.cos(yaw)
    yaw_sin = math.sin(yaw)
    resolution = max(1e-6, float(grid["resolution"]))

    def grid_to_world(gx: float, gy: float) -> Tuple[float, float]:
        x_local = gx * resolution
        y_local = gy * resolution
        return (
            float(grid["origin_x"]) + yaw_cos * x_local - yaw_sin * y_local,
            float(grid["origin_y"]) + yaw_sin * x_local + yaw_cos * y_local,
        )

    cell_specs = []
    world_bounds = []
    for r in range(0, rows, stride):
        for c in range(0, cols, stride):
            occupied = False
            free = False
            for rr in range(r, min(rows, r + stride)):
                base = rr * cols
                for cc in range(c, min(cols, c + stride)):
                    if base + cc >= len(data):
                        continue
                    val = int(data[base + cc])
                    if val >= 50:
                        occupied = True
                    elif val == 0:
                        free = True
            if occupied:
                fill = "#111827"
                opacity = "0.95"
            elif free:
                fill = "#f4f7f5"
                opacity = "1.0"
            else:
                continue
            corners = (
                grid_to_world(float(c), float(r)),
                grid_to_world(float(min(cols, c + stride)), float(r)),
                grid_to_world(float(min(cols, c + stride)), float(min(rows, r + stride))),
                grid_to_world(float(c), float(min(rows, r + stride))),
            )
            cell_specs.append((corners, fill, opacity))
            world_bounds.extend(corners)

    path_world = [(float(x), float(y)) for x, y in path]
    bounds_points = world_bounds + path_world
    if bounds_points:
        min_x = min(p[0] for p in bounds_points)
        max_x = max(p[0] for p in bounds_points)
        min_y = min(p[1] for p in bounds_points)
        max_y = max(p[1] for p in bounds_points)
    else:
        min_x, max_x, min_y, max_y = 0.0, float(cols), 0.0, float(rows)
    pad = max(4.0, 0.04 * max(max_x - min_x, max_y - min_y, 1.0))
    min_x -= pad
    max_x += pad
    min_y -= pad
    max_y += pad
    scale = min(mw / max(1e-6, max_x - min_x), mh / max(1e-6, max_y - min_y))
    draw_w = (max_x - min_x) * scale
    draw_h = (max_y - min_y) * scale
    ox = mx + (mw - draw_w) * 0.5
    oy = my + (mh - draw_h) * 0.5

    def wp(wx: float, wy: float) -> Tuple[float, float]:
        return ox + (wx - min_x) * scale, oy + (max_y - wy) * scale

    cells = []
    for corners, fill, opacity in cell_specs:
        points = " ".join(f"{px:.2f},{py:.2f}" for px, py in (wp(x, y) for x, y in corners))
        cells.append(
            f'<polygon points="{points}" fill="{fill}" opacity="{opacity}" />'
        )

    path_markup = ""
    if len(path_world) >= 2:
        pts = [f"{px:.1f},{py:.1f}" for px, py in (wp(x, y) for x, y in path_world)]
        if len(pts) >= 2:
            joined = " ".join(pts)
            path_markup = (
                f'<polyline points="{joined}" fill="none" stroke="#bcf4df" stroke-width="15" stroke-linecap="round" stroke-linejoin="round" />'
                f'<polyline points="{joined}" fill="none" stroke="{PATH_GREEN}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />'
            )

    return f"""
    <svg viewBox="0 0 {width} {height}" class="w-full h-[440px]">
      <rect x="10" y="10" width="500" height="410" rx="28" fill="#f7fffb" stroke="#caeee2" />
      <rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="8" fill="#dfe8e4" />
      {''.join(cells)}
      {path_markup}
      <text x="260" y="24" text-anchor="middle" fill="{MUTED}" font-size="13" font-weight="700">{status}</text>
      <text x="260" y="414" text-anchor="middle" fill="{MUTED}" font-size="13" font-weight="700">Actual /navivest/occupancy_grid + /navivest/path ({len(path)} path points)</text>
    </svg>
    """


def topdown_svg(state: Dict[str, Any]) -> str:
    width, height = 520, 440
    mx, my, mw, mh = 40, 32, 440, 360

    def px(point: Dict[str, float]) -> tuple[float, float]:
        x = float(point.get("x", 0.0))
        y = float(point.get("y", 0.0))
        sx = mx + mw * (0.5 + max(-0.46, min(0.46, x / 3.2)))
        sy = my + mh - 28 - max(0.0, min(1.0, y / 5.0)) * (mh - 56)
        return sx, sy

    illustrated_path = [
        {"x": 0.0, "y": 0.0},
        {"x": -0.06, "y": 0.75},
        {"x": -0.34, "y": 1.35},
        {"x": -0.58, "y": 2.10},
        {"x": -0.48, "y": 2.85},
        {"x": -0.20, "y": 3.55},
        {"x": 0.0, "y": 4.75},
    ]
    illustrated_obstacles = [
        {"x": 0.0, "y": 2.35, "type": "chair"},
    ]

    path_points = " ".join(f"{x:.1f},{y:.1f}" for x, y in [px(p) for p in illustrated_path])
    obstacles = []
    for obs in illustrated_obstacles:
        ox, oy = px(obs)
        label = str(obs.get("type", "obstacle")).title()
        obstacles.append(
            f'<rect x="{ox-40:.1f}" y="{oy-28:.1f}" width="80" height="56" rx="12" fill="{OBSTACLE}" opacity="0.92" />'
            f'<rect x="{ox-54:.1f}" y="{oy-42:.1f}" width="108" height="28" rx="10" fill="#f15555" opacity="0.72" />'
            f'<text x="{ox:.1f}" y="{oy+5:.1f}" text-anchor="middle" fill="white" font-size="13" font-weight="800">{label}</text>'
            f'<text x="{ox:.1f}" y="{oy-22:.1f}" text-anchor="middle" fill="white" font-size="12" font-weight="800">Blocked</text>'
        )

    path_markup = ""
    if path_points:
        path_markup = (
            f'<polyline points="{path_points}" fill="none" stroke="#c5eadf" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" />'
            f'<polyline points="{path_points}" fill="none" stroke="{PATH_GREEN}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" />'
        )

    ux, uy = px({"x": 0.0, "y": 0.0})
    return f"""
    <svg viewBox="0 0 {width} {height}" class="w-full h-[440px]">
      <rect x="10" y="10" width="500" height="410" rx="28" fill="#f7fffb" stroke="#caeee2" />
      <rect x="{mx + mw*0.18}" y="{my}" width="{mw*0.64}" height="{mh}" rx="28" fill="#eefcf6" />
      <rect x="{mx}" y="{my+6}" width="{mw*0.15}" height="{mh-12}" rx="18" fill="#fff0ec" />
      <rect x="{mx+mw*0.85}" y="{my+6}" width="{mw*0.15}" height="{mh-12}" rx="18" fill="#fff0ec" />
      <text x="{mx+18}" y="{my+28}" fill="#c0564a" font-size="12" font-weight="700">blocked</text>
      <text x="{mx+mw-18}" y="{my+28}" fill="#c0564a" font-size="12" font-weight="700" text-anchor="end">blocked</text>
      {''.join(obstacles)}
      {path_markup}
      <circle cx="{ux}" cy="{uy}" r="25" fill="{TEXT}" stroke="white" stroke-width="4" />
      <text x="{ux}" y="{uy+4}" text-anchor="middle" fill="white" font-size="12" font-weight="800">Vest</text>
      <line x1="{ux}" y1="{uy-44}" x2="{ux}" y2="{uy-85}" stroke="{TEXT}" stroke-width="4" marker-end="url(#arrow)" />
      <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="4" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="{TEXT}" /></marker></defs>
      <text x="260" y="22" text-anchor="middle" fill="{MUTED}" font-size="13" font-weight="700">Top-down demo illustration</text>
      <text x="260" y="414" text-anchor="middle" fill="{MUTED}" font-size="13" font-weight="700">User position</text>
    </svg>
    """


def topdown_card(state: Dict[str, Any]) -> None:
    with card().classes("p-5"):
        with ui.row().classes("items-center justify-between w-full"):
            ui.label("Top-Down Path View").classes("text-xl font-black text-slate-900")
            ui.badge("Illustration", color="teal")
        ui.html(topdown_svg(state))


def haptic_vest(state: Dict[str, Any]) -> None:
    zones = state.get("hapticZones", {}) or {}
    cue = str(state.get("audioCue", "")).upper()
    active = RED if cue in {"STOP", "WAIT"} else ACCENT

    def motor(active_on: bool, label: str) -> str:
        color = active if active_on else "#d8dee9"
        text = "white" if active_on else MUTED
        return f'<div class="motor" style="background:{color};color:{text}">{label}</div>'

    with card().classes("p-5"):
        ui.label("Haptic Vest Feedback").classes("text-xl font-black text-slate-900")
        ui.html(f"""
        <div class="vest-wrap">
          <div class="vest-strap left"></div><div class="vest-strap right"></div>
          <div class="vest-body">
            <div class="shoulder left">{motor(bool(zones.get('left_shoulder')), 'LS')}</div>
            <div class="shoulder right">{motor(bool(zones.get('right_shoulder')), 'RS')}</div>
            <div class="back-side left">{motor(bool(zones.get('left_back')), 'LB')}</div>
            <div class="back-side right">{motor(bool(zones.get('right_back')), 'RB')}</div>
            <div class="vest-label">NaviVest</div>
          </div>
        </div>
        """)
        ui.label("Four motors: left/right shoulder and left/right back side.").classes("text-sm font-semibold text-slate-800 mt-2")


def control_panel(state: Dict[str, Any]) -> None:
    global svo_select, manual_path, launch_btn, stop_btn
    with card().classes("p-5"):
        ui.label("Play a Prerecorded SVO").classes("text-xl font-black text-slate-900")
        ui.label("Select a saved recording, then press Play Demo. No live camera feed is used.").classes("text-slate-600")

        paths = controller.scan_svos()
        options = {path: Path(path).name for path in paths}
        current = str(controller.selected_svo) if controller.selected_svo and str(controller.selected_svo) in options else None
        svo_select = ui.select(options=options, value=current, label="Choose from SVO folder").props("outlined dense clearable").classes("w-full mt-4 min-w-0")

        def select_from_dropdown(e: Any) -> None:
            if e.value:
                controller.set_selected_svo(str(e.value))
                refresh()

        svo_select.on_value_change(select_from_dropdown)

        manual_path = ui.input(
            "Or paste/type full SVO path",
            value=controller.manual_svo_text,
            placeholder="/home/macho/navivest_svos/chair_walkway.svo2",
        ).props("outlined dense clearable").classes("w-full mt-3")

        def remember_manual_path(e: Any) -> None:
            # Keep partially typed text across the auto-refresh timer.
            controller.manual_svo_text = str(e.value or "")

        manual_path.on_value_change(remember_manual_path)

        def apply_manual_path() -> None:
            controller.set_selected_svo(str(manual_path.value or ""))
            refresh()

        with ui.row().classes("w-full items-center gap-2 mt-2"):
            ui.button("Use Typed Path", icon="check", on_click=apply_manual_path).props("unelevated").classes("bg-orange-100 text-orange-800")
            ui.label("Path is read on this computer, not from a live camera.").classes("text-xs text-slate-500")

        with ui.row().classes("gap-3 mt-3"):
            launch_btn = ui.button("Play Demo", icon="play_arrow", on_click=lambda: (controller.set_selected_svo(controller.manual_svo_text) if controller.manual_svo_text.strip() else None, controller.play(), refresh())).classes(
                "bg-orange-500 text-white font-bold px-6"
            )
            stop_btn = ui.button("Stop", icon="stop", on_click=lambda: (controller.stop(), refresh())).classes(
                "bg-red-500 text-white font-bold px-5"
            )
            ui.button("Refresh Files", icon="refresh", on_click=refresh).props("outline").classes("text-slate-700")

        ui.linear_progress(float(state.get("progress", 0))).classes("mt-4 rounded-full")
        with ui.row().classes("justify-between w-full text-sm text-slate-500"):
            ui.label(str(state.get("timestamp", "00:00")))
            ui.label(str(state.get("duration", "01:10")))

        selected_name = controller.selected_svo.name if controller.selected_svo else "No SVO selected"
        selected_path = str(controller.selected_svo) if controller.selected_svo else ""
        ui.label(f"Selected: {selected_name}").classes("text-xs text-slate-500 mt-2 truncate max-w-full").tooltip(selected_path)
        ui.label(controller.status).classes("text-sm font-semibold text-slate-700 mt-1")


def instructions_card() -> None:
    with card().classes("p-5"):
        ui.label("Visitor Flow").classes("text-xl font-black text-slate-900")
        steps = [
            "Presenter selects a prerecorded SVO file.",
            "Press Play Demo to launch the recording.",
            "Watch the safe path and guidance cue update.",
            "Feel the haptic motors activate on the vest/controller.",
        ]
        for i, text in enumerate(steps, 1):
            with ui.row().classes("items-start gap-3 mt-3"):
                ui.badge(str(i), color="orange").classes("rounded-full")
                ui.label(text).classes("text-slate-700")


def status_panel(state: Dict[str, Any]) -> None:
    grid, path, status = controller.ros_snapshot()
    with card().classes("p-5"):
        ui.label("System Status").classes("text-xl font-black text-slate-900")
        status_chip("SVO loaded", "Ready" if state.get("svoLoaded") else "Select file", bool(state.get("svoLoaded")))
        status_chip("Depth playback", "Playing" if state.get("depthPlaybackActive") else "Paused", bool(state.get("depthPlaybackActive")))
        status_chip("Planner", "Active" if state.get("plannerActive") else "Waiting", bool(state.get("plannerActive")))
        status_chip("Audio cues", "Cue active" if state.get("audioCue") not in {"READY", ""} else "Ready", True)
        status_chip("Haptic feedback", "Connected", True)
        status_chip("ROS grid", "Live" if grid is not None else "Waiting", grid is not None)
        status_chip("ROS path", f"{len(path)} pts" if path else "Waiting", bool(path))
        ui.label(status).classes("text-xs text-slate-500 mt-3 break-words")
        log = controller.recent_launch_log()
        if log:
            ui.textarea(value=log).props("readonly autogrow").classes("w-full text-xs mt-2")


def how_it_works() -> None:
    with card().classes("p-5"):
        ui.label("What NaviVest Is Doing").classes("text-xl font-black text-slate-900")
        items = [
            ("movie", "Replay depth scene", "Loads a prerecorded ZED SVO walking scenario."),
            ("search", "Detect obstacles", "Finds objects and blocked walking areas."),
            ("route", "Plan a safe path", "Chooses a safer route around obstacles."),
            ("vibration", "Guide with sound + touch", "Uses audio cues and vibration motors."),
        ]
        for icon, title, body in items:
            with ui.row().classes("items-start gap-3 mt-3"):
                ui.icon(icon, color="teal").classes("text-2xl")
                with ui.column().classes("gap-0"):
                    ui.label(title).classes("font-bold text-slate-800")
                    ui.label(body).classes("text-sm text-slate-500")


def why_card() -> None:
    with card().classes("p-5"):
        ui.label("Why This Matters").classes("text-xl font-black text-slate-900")
        ui.label(
            "NaviVest explores how wearable depth sensing and haptic feedback can help visually impaired users understand nearby obstacles without needing to look at a screen. This booth demo uses prerecorded scenarios to show the full guidance loop safely and reliably."
        ).classes("text-slate-700 leading-relaxed")


def refresh() -> None:
    controller.tick()
    if main_view is not None:
        main_view.refresh()


def periodic_refresh() -> None:
    """Refresh the live display without fighting file selection/editing.

    Rebuilding the full NiceGUI view every 0.5 seconds destroys and recreates
    the select/input widgets. That makes dropdown selection and typing a path
    feel broken, so only the live ROS panels are refreshed here. They must keep
    updating even if the launch process has already exited but ROS topics are
    still publishing.
    """
    controller.tick()
    live_guidance_card.refresh()
    live_topdown_card.refresh()
    live_haptic_vest.refresh()
    live_status_panel.refresh()


@ui.refreshable
def live_guidance_card() -> None:
    guidance_card(controller.current_state())


@ui.refreshable
def live_topdown_card() -> None:
    topdown_card(controller.current_state())


@ui.refreshable
def live_haptic_vest() -> None:
    haptic_vest(controller.current_state())


@ui.refreshable
def live_status_panel() -> None:
    status_panel(controller.current_state())


@ui.refreshable
def render() -> None:
    state = controller.current_state()
    cue = str(state.get("audioCue", "READY")).upper()
    _arrow, cue_color, _text = CUE_META.get(cue, ("●", TEAL, "Ready."))

    with ui.column().classes("w-full max-w-[1800px] mx-auto min-h-screen p-4 md:p-6 gap-5"):
        with ui.row().classes("w-full items-center justify-between rounded-[28px] bg-white shadow-sm border border-orange-100 p-6"):
            with ui.column().classes("gap-1"):
                ui.label("NaviVest").classes("text-5xl font-black text-slate-900")
                ui.label("A wearable navigation assistant that uses depth vision, path planning, audio, and vibration cues to guide users around obstacles.").classes(
                    "text-lg text-slate-600"
                )
            with ui.column().classes("items-end gap-2"):
                ui.badge("Demo Mode: Prerecorded SVO", color="teal").classes("text-sm px-4 py-2")
                ui.badge("Stable booth playback", color="orange").classes("text-sm px-4 py-2")
                ui.badge("No live camera required", color="blue").classes("text-sm px-4 py-2")

        with ui.grid(columns=12).classes("w-full gap-5 auto-rows-auto"):
            with ui.column().classes("col-span-12 xl:col-span-4 gap-5"):
                control_panel(state)
                instructions_card()
                why_card()

            with ui.column().classes("col-span-12 xl:col-span-5 gap-5"):
                live_guidance_card()
                live_topdown_card()

            with ui.column().classes("col-span-12 xl:col-span-3 gap-5"):
                how_it_works()
                live_haptic_vest()
                live_status_panel()

        ui.html(f'<style>:root{{--cue-color:{cue_color};}}</style>')


def build_app(args: argparse.Namespace) -> None:
    global controller, main_view
    controller = DemoController(
        svo_dir=args.svo_dir,
        data_path=args.data,
        launch_command=args.launch_command,
    )

    ui.add_head_html("""
    <style>
      body { background: radial-gradient(circle at top right, #fff0d8 0, #fff8ec 36%, #eafbf5 100%); }
      .nicegui-content { background: transparent; }
      .q-card { box-shadow: 0 8px 26px rgba(112, 74, 28, 0.10); }
      .pulse-dot {
        width: 108px; height: 108px; border-radius: 999px; display:flex; align-items:center; justify-content:center;
        color:white; font-size:52px; font-weight:900; box-shadow: 0 0 0 0 color-mix(in srgb, var(--cue-color) 35%, transparent);
        animation: pulse 1.25s infinite;
      }
      @keyframes pulse { 0% { transform: scale(.96); } 50% { transform: scale(1.04); } 100% { transform: scale(.96); } }
      .vest-wrap { height: 230px; position:relative; display:flex; align-items:center; justify-content:center; }
      .vest-body { width:150px; height:165px; border-radius:32px; background:#1f2937; position:relative; margin-top:28px; }
      .vest-strap { width:24px; height:100px; background:#1f2937; border-radius:20px; position:absolute; top:25px; }
      .vest-strap.left { transform: rotate(28deg); margin-left:-140px; }
      .vest-strap.right { transform: rotate(-28deg); margin-left:140px; }
      .motor { width:38px; height:38px; border-radius:999px; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:11px; border:3px solid #fff3; }
      .shoulder { position:absolute; top:20px; }
      .shoulder.left { left:22px; }
      .shoulder.right { right:22px; }
      .back-side { position:absolute; bottom:72px; }
      .back-side.left { left:26px; }
      .back-side.right { right:26px; }
      .vest-label { position:absolute; bottom:26px; left:34px; right:34px; text-align:center; color:#dbeafe; background:#334155; border-radius:12px; padding:6px; font-size:12px; font-weight:800; }
      .q-field__native, .q-field__input { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
    </style>
    """)
    main_view = render
    start_ros_monitor()
    render()
    ui.timer(0.5, periodic_refresh)
    app.on_shutdown(lambda: controller.stop())


def main() -> None:
    parser = argparse.ArgumentParser(description="NaviVest NiceGUI SVO booth demo")
    parser.add_argument("--svo-dir", type=Path, default=Path("/home/macho/navivest_datasets/recordings"), help="Directory containing prerecorded .svo/.svo2 files")
    parser.add_argument("--data", type=Path, default=None, help="Optional JSON state file produced by the backend")
    parser.add_argument("--launch-command", default=DEFAULT_LAUNCH_COMMAND, help="Command template. Use {svo} where the quoted SVO path should go")
    parser.add_argument("--host", default="0.0.0.0", help="NiceGUI host")
    parser.add_argument("--port", type=int, default=8080, help="NiceGUI port")
    args = parser.parse_args()

    build_app(args)
    ui.run(host=args.host, port=args.port, title="NaviVest SVO Demo", reload=False, show=True)


if __name__ == "__main__":
    main()
