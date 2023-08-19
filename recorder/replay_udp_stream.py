from __future__ import annotations

import argparse
import pickle
import socket
import time
from io import BufferedReader
from io import BytesIO

from .utils import open_socket


def _replay_data(s: socket.socket, data: BytesIO | BufferedReader, addr: tuple):
    while True:
        try:
            record = pickle.load(data)
            timing, message = record
            time.sleep(timing)
            s.sendto(message, addr)
        except (EOFError, pickle.UnpicklingError):
            break
        except Exception as e:
            print(f"Event failed with error '{e}'")
            pass


def main(file_name: str, addr: tuple):
    if isinstance(file_name, BytesIO):
        with open_socket() as s:
            _replay_data(s, file_name, addr)
    else:
        with open_socket() as s, open(file_name, "rb") as f:
            _replay_data(s, f, addr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send UDP file captured previously using UDPReceive.py",
    )
    parser.add_argument("-p", "--port", help="Port to listen", required=False, type=int, default=1234)
    parser.add_argument("-f", "--file", help="File to send", required=False, type=str, default="udp.bin")
    parser.add_argument("-s", "--server", help="Host target", required=False, type=str, default="127.0.0.1")

    args = parser.parse_args()

    addr = (args.server, args.port)
    main(args.file, addr)
