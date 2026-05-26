#!/usr/bin/env python3

import os
import signal
import subprocess
import threading
import time
from pathlib import Path
from typing import Optional

from nicegui import app, ui


WORKSPACE = Path("/home/macho/navivest_ws")
SETUP_BASH = WORKSPACE / "install" / "setup.bash"
DATASET_DIR = Path("/home/macho/navivest_datasets/recordings")
DEFAULT_SVO = "01_open_hallway.svo2"
GUIDANCE_START_M = "0.10"


class DemoState:
    def __init__(self):
        self.lock = threading.Lock()
        self.process: Optional[subprocess.Popen] = None
        self.status = "Idle"
        self.latest_guidance = "-"
        self.latest_audio = "-"
        self.latest_haptic = "-"
        self.log_lines = []
        self.ros_node = None

    def set_status(self, status: str):
        with self.lock:
            self.status = status

    def append_log(self, line: str):
        line = line.rstrip()
        if not line:
            return
        with self.lock:
            self.log_lines.append(line)
            self.log_lines = self.log_lines[-80:]

    def snapshot(self):
        with self.lock:
            return {
                "running": self.process is not None and self.process.poll() is None,
                "status": self.status,
                "guidance": self.latest_guidance,
                "audio": self.latest_audio,
                "haptic": self.latest_haptic,
                "logs": "\n".join(self.log_lines[-40:]),
            }


state = DemoState()


def svo_files():
    if not DATASET_DIR.is_dir():
        return [DEFAULT_SVO]
    files = sorted(
        p.name for p in DATASET_DIR.iterdir() if p.suffix.lower() in {".svo", ".svo2"}
    )
    return files or [DEFAULT_SVO]


def haptic_command_for_phrase(phrase: str) -> str:
    text = phrase.strip().upper()
    if not text:
        return "STOP"
    if text.startswith("LEFT") or text.startswith("BEAR LEFT"):
        return "LEFT"
    if text.startswith("RIGHT") or text.startswith("BEAR RIGHT"):
        return "RIGHT"
    if text.startswith("FORWARD"):
        return "FORWARD"
    if text == "PATH CLEAR":
        return "FORWARD"
    if text.startswith(("WAIT", "STOP", "BLOCKED")) or "NO SAFE PATH" in text:
        return "STOP"
    return "STOP"


def start_svo_demo(svo_name: str):
    snap = state.snapshot()
    if snap["running"]:
        ui.notify("SVO demo is already running", type="warning")
        return

    if not SETUP_BASH.is_file():
        ui.notify(f"Missing ROS setup file: {SETUP_BASH}", type="negative")
        return

    command = (
        f"source {SETUP_BASH} && "
        "ros2 launch navivest_bringup navivest_full_svo.launch.py "
        f"svo_name:={svo_name} guidance_start_m:={GUIDANCE_START_M}"
    )
    state.append_log(f"$ {command}")
    state.set_status(f"Starting SVO demo: {svo_name}")

    process = subprocess.Popen(
        ["bash", "-lc", command],
        cwd=str(WORKSPACE),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        start_new_session=True,
    )
    with state.lock:
        state.process = process

    threading.Thread(target=read_process_output, args=(process,), daemon=True).start()


def read_process_output(process: subprocess.Popen):
    try:
        assert process.stdout is not None
        for line in process.stdout:
            state.append_log(line)
    finally:
        code = process.wait()
        with state.lock:
            if state.process is process:
                state.process = None
        state.set_status(f"Demo exited with code {code}")


def stop_demo():
    with state.lock:
        process = state.process
    if process is None or process.poll() is not None:
        state.set_status("Idle")
        return

    state.set_status("Stopping demo")
    try:
        os.killpg(process.pid, signal.SIGINT)
    except ProcessLookupError:
        return

    def force_kill_if_needed():
        try:
            process.wait(timeout=5.0)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass

    threading.Thread(target=force_kill_if_needed, daemon=True).start()


def start_ros_monitor():
    try:
        import rclpy
        from rclpy.node import Node
        from std_msgs.msg import String
    except Exception as exc:
        state.append_log(f"ROS topic monitor disabled: {exc}")
        return

    class GuiMonitor(Node):
        def __init__(self):
            super().__init__("navivest_demo_gui_monitor")
            self.create_subscription(String, "/navivest/guidance", self.guidance_cb, 10)
            self.create_subscription(String, "/navivest/audio_cue", self.audio_cb, 10)

        def guidance_cb(self, msg):
            with state.lock:
                state.latest_guidance = msg.data.strip() or "-"

        def audio_cb(self, msg):
            audio = msg.data.strip() or "-"
            haptic = haptic_command_for_phrase(audio)
            with state.lock:
                state.latest_audio = audio
                state.latest_haptic = haptic

    def spin():
        try:
            rclpy.init(args=None)
            node = GuiMonitor()
            state.ros_node = node
            rclpy.spin(node)
        except Exception as exc:
            state.append_log(f"ROS topic monitor stopped: {exc}")
        finally:
            try:
                if state.ros_node is not None:
                    state.ros_node.destroy_node()
            except Exception:
                pass
            try:
                if rclpy.ok():
                    rclpy.shutdown()
            except Exception:
                pass

    threading.Thread(target=spin, daemon=True).start()


@ui.page("/")
def main_page():
    files = svo_files()
    default = DEFAULT_SVO if DEFAULT_SVO in files else files[0]

    ui.add_head_html(
        """
        <style>
          body { background: #101418; }
          .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
        </style>
        """
    )

    with ui.column().classes("w-full max-w-5xl mx-auto p-6 gap-5"):
        ui.label("NaviVest SVO Demo").classes("text-3xl font-bold text-white")
        ui.label("Launch the existing SVO playback pipeline and monitor guidance outputs.").classes(
            "text-slate-300"
        )

        with ui.card().classes("w-full bg-slate-900 text-white"):
            with ui.row().classes("items-end gap-4"):
                selected_svo = ui.select(files, value=default, label="SVO recording").classes(
                    "w-80"
                )
                ui.button(
                    "Run SVO Demo",
                    on_click=lambda: start_svo_demo(selected_svo.value),
                ).props("color=green")
                ui.button("Stop", on_click=stop_demo).props("color=red outline")

            status_label = ui.label().classes("text-lg font-semibold")

        with ui.grid(columns=3).classes("w-full gap-4"):
            with ui.card().classes("bg-slate-900 text-white"):
                ui.label("Immediate Guidance").classes("text-slate-300")
                guidance_label = ui.label("-").classes("text-4xl font-bold")
            with ui.card().classes("bg-slate-900 text-white"):
                ui.label("Audio Cue").classes("text-slate-300")
                audio_label = ui.label("-").classes("text-4xl font-bold")
            with ui.card().classes("bg-slate-900 text-white"):
                ui.label("Haptic Command").classes("text-slate-300")
                haptic_label = ui.label("-").classes("text-4xl font-bold")

        with ui.card().classes("w-full bg-slate-900 text-white"):
            ui.label("Launch Log").classes("text-slate-300")
            log_area = ui.textarea(value="").classes("w-full mono").props(
                "readonly autogrow input-class=mono"
            )

    def refresh():
        snap = state.snapshot()
        status_label.text = snap["status"]
        guidance_label.text = snap["guidance"]
        audio_label.text = snap["audio"]
        haptic_label.text = snap["haptic"]
        log_area.value = snap["logs"]

    ui.timer(0.25, refresh)


def shutdown():
    stop_demo()


app.on_shutdown(shutdown)


if __name__ in {"__main__", "__mp_main__"}:
    start_ros_monitor()
    ui.run(title="NaviVest Demo", host="0.0.0.0", port=8080, reload=False)
