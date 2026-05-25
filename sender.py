#!/usr/bin/env python3

import argparse
import socket
import sys


DEFAULT_PORT = 5000


def send_command(sock, command):
    message = command.strip().upper()
    if not message:
        return
    sock.sendall((message + "\n").encode("utf-8"))


def interactive_sender(sock):
    print("Enter commands like LEFT, RIGHT, FORWARD, STOP.")
    print("Press Ctrl-D or submit an empty line to quit.")

    while True:
        try:
            command = input("Message: ").strip()
        except EOFError:
            break

        if not command:
            break

        send_command(sock, command)


def main():
    parser = argparse.ArgumentParser(description="Send vibration commands to the Jetson receiver over TCP.")
    parser.add_argument("host", help="Receiver IP address or hostname")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Receiver TCP port (default: {DEFAULT_PORT})")
    parser.add_argument("commands", nargs="*", help="Optional commands to send without interactive prompts")
    args = parser.parse_args()

    with socket.create_connection((args.host, args.port), timeout=5) as sock:
        if args.commands:
            for command in args.commands:
                send_command(sock, command)
        else:
            interactive_sender(sock)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())