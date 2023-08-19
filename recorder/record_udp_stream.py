from __future__ import annotations

import argparse
import pickle
import signal
import socket
import sys
import time
from io import BytesIO

from .utils import open_socket


def _signal_handler(signal, frame):
    raise SystemExit("Scoket is closed")


def _record_data(s, f, max_num_packets=1e9, max_seconds=1e9, buffer_size=65536):
    start_time = time.time()
    previous_time = start_time
    num_packets = 0

    while 1:
        try:
            msg, _ = s.recvfrom(buffer_size)
            received_at = time.time()
            time_until_msg = received_at - previous_time
            pickle.dump((time_until_msg, msg), f)

            previous_time = received_at
            num_packets += 1

            end_condition = (num_packets >= max_num_packets) | (received_at - start_time > max_seconds)

            if end_condition:
                break
        except SystemExit:
            break


def _prepare_socket(s: socket.socket, addr: tuple):
    try:
        s.bind(addr)
        print(f"Socket bind complete on port {addr}")
        print("Press Ctrl+C to stop capturing")
    except OSError as e:
        print(f"Bind failed. Error Code : {e}")
        sys.exit(1)

    s.setblocking(True)


def main(file_name: str, addr: tuple, buffer_size=65536, max_num_packets=1e9, max_seconds=1e9):
    signal.signal(signal.SIGINT, _signal_handler)
    with open_socket() as s:
        _prepare_socket(s, addr)
        if isinstance(file_name, BytesIO):
            _record_data(s, file_name, max_num_packets, max_seconds, buffer_size)
        else:
            with open(file_name, "wb") as f:
                _record_data(s, f, max_num_packets, max_seconds, buffer_size)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Capture UDP packets for further analysis and playback",
    )
    parser.add_argument("-p", "--server", help="Host to listen to", required=False, type=str, default="127.0.0.1")
    parser.add_argument("-p", "--port", help="Port to listen to", required=False, type=int, default=1234)
    parser.add_argument("-f", "--file", help="File to write data to", required=False, type=str, default="udp.bin")
    parser.add_argument("-b", "--buffer", help="Host target", required=False, type=int, default=65536)
    parser.add_argument(
        "-c",
        "--count",
        help="Stop capture after x packets",
        required=False,
        type=int,
        default=1000000000,
    )
    parser.add_argument(
        "-s",
        "--seconds",
        help="Stop capture after x seconds",
        required=False,
        type=int,
        default=1000000000,
    )

    args = parser.parse_args()

    addr = (args.server, args.port)
    main(file_name=args.file, addr=addr, buffer_size=args.buffer, max_num_packets=args.count, max_seconds=args.seconds)
