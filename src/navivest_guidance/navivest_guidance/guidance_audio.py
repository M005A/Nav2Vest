#!/usr/bin/env python3

import queue
import socket
import subprocess
import threading
import time
from typing import Optional

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


HAPTICS_HOST = "10.0.0.50"
HAPTICS_PORT = 5000
HAPTICS_ENABLED = True
HAPTICS_TIMEOUT_S = 0.3
HAPTICS_ERROR_LOG_PERIOD_S = 5.0


class GuidanceAudio(Node):
    """Speak NaviVest audio cues without overlapping sentences.

    The planner publishes one guarded cue on /navivest/audio_cue. This node
    keeps the spoken output serialized: it lets the current sentence finish,
    keeps only the newest pending cue, and suppresses rapid duplicates.
    """

    def __init__(self):
        super().__init__("guidance_audio")

        self.declare_parameter("topic", "/navivest/audio_cue")
        self.declare_parameter("min_repeat_s", 1.5)
        self.declare_parameter("voice_cmd", "spd-say")
        self.declare_parameter("use_spd_wait", True)

        self.last_spoken: Optional[str] = None
        self.last_spoken_time = 0.0
        self.pending: Optional[str] = None
        self.last_haptics_error_log = 0.0
        self.lock = threading.Lock()
        self.wakeup = threading.Event()
        self.shutdown_requested = False

        topic = str(self.get_parameter("topic").value)
        self.sub = self.create_subscription(String, topic, self.cb, 10)

        self.worker = threading.Thread(target=self.speech_worker, daemon=True)
        self.worker.start()

        self.get_logger().info(f"Speaking guidance cues from {topic}")

    def cb(self, msg: String):
        phrase = self.normalize_phrase(msg.data)
        if not phrase:
            return

        now = time.time()
        min_repeat_s = float(self.get_parameter("min_repeat_s").value)

        with self.lock:
            # Drop rapid exact duplicates. This prevents repeated "Forward" or
            # "Left in 0.5 meters" updates from filling the queue.
            if phrase == self.last_spoken and now - self.last_spoken_time < min_repeat_s:
                return
            if phrase == self.pending:
                return
            # Keep only the newest cue while the current sentence is speaking.
            # Old pending cues may no longer be relevant by the time speech frees up.
            self.pending = phrase
            self.wakeup.set()

    def normalize_phrase(self, text: str) -> str:
        raw = text.strip()
        if not raw:
            return ""

        upper = raw.upper()
        fixed = {
            "STOP": "Wait",
            "STOP!": "Wait",
            "WAIT": "Wait",
            "FORWARD": "Forward",
            "LEFT": "Left",
            "RIGHT": "Right",
        }
        if upper in fixed:
            return fixed[upper]

        # Preserve richer planner cues such as "Left in 0.5 meters".
        words = raw.split()
        if not words:
            return ""
        words[0] = words[0].capitalize()
        return " ".join(words)

    def speech_worker(self):
        while not self.shutdown_requested:
            self.wakeup.wait(timeout=0.2)
            self.wakeup.clear()

            while True:
                with self.lock:
                    phrase = self.pending
                    self.pending = None

                if not phrase:
                    break

                self.send_haptic_command(phrase)
                self.speak_blocking(phrase)
                with self.lock:
                    self.last_spoken = phrase
                    self.last_spoken_time = time.time()

                # Loop once more in case a newer cue arrived while speaking.

    def haptic_command_for_phrase(self, phrase: str) -> str:
        text = phrase.strip().upper()
        if not text:
            return "STOP"
        if text.startswith("LEFT"):
            return "LEFT"
        if text.startswith("RIGHT"):
            return "RIGHT"
        if text == "FORWARD" or text.startswith("FORWARD"):
            return "FORWARD"
        if text.startswith(("WAIT", "STOP", "BLOCKED")) or "NO SAFE PATH" in text:
            return "STOP"
        return "STOP"

    def send_haptic_command(self, phrase: str):
        if not HAPTICS_ENABLED:
            return

        command = self.haptic_command_for_phrase(phrase)
        payload = f"{command}\n".encode("utf-8")
        try:
            with socket.create_connection(
                (HAPTICS_HOST, HAPTICS_PORT),
                timeout=HAPTICS_TIMEOUT_S,
            ) as sock:
                sock.settimeout(HAPTICS_TIMEOUT_S)
                sock.sendall(payload)
        except OSError as exc:
            now = time.time()
            if now - self.last_haptics_error_log >= HAPTICS_ERROR_LOG_PERIOD_S:
                self.get_logger().warn(
                    f"Haptics TCP send failed to {HAPTICS_HOST}:{HAPTICS_PORT}: {exc}"
                )
                self.last_haptics_error_log = now

    def speak_blocking(self, phrase: str):
        voice_cmd = str(self.get_parameter("voice_cmd").value)
        use_spd_wait = bool(self.get_parameter("use_spd_wait").value)

        if voice_cmd == "spd-say" and use_spd_wait:
            cmd = [voice_cmd, "-w", phrase]
        else:
            cmd = [voice_cmd, phrase]

        try:
            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        except FileNotFoundError:
            self.get_logger().error(
                f"Voice command '{voice_cmd}' not found. Install speech-dispatcher or use espeak."
            )
            time.sleep(1.0)

    def destroy_node(self):
        self.shutdown_requested = True
        self.wakeup.set()
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = GuidanceAudio()
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
