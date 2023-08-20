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
    """
    A signal handler function that is called when a specific signal is received.
    This is used when the signal of end of stream is received

    Args:
        signal: The signal number that triggered the handler.
        frame: The current execution frame.

    Raises:
        SystemExit: If the signal is received, this exception is raised with the message "Socket is closed".
    """
    raise SystemExit("Scoket is closed")


def _record_data(s, f, max_num_packets=1e9, max_seconds=1e9, buffer_size=65536):
    """
    Records data received from a socket and saves it to a file.

    Args:
        s (socket): The socket object to receive data from.
        f (file): The file object to write the received data to.
        max_num_packets (int, optional): The maximum number of packets to receive. Default is 1e9.
        max_seconds (int, optional): The maximum number of seconds to receive data. Default is 1e9.
        buffer_size (int, optional): The size of the buffer for receiving data. Default is 65536.

    Returns:
        None
    """
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
    """
    Binds the given socket to the specified address and sets it to blocking mode.

    Args:
        s (socket.socket): The socket object to bind.
        addr (tuple): The address to bind the socket to.

    Raises:
        OSError: If the bind operation fails.

    Returns:
        None
    """
    try:
        s.bind(addr)
        print(f"Socket bind complete on port {addr}")
        print("Press Ctrl+C to stop capturing")
    except OSError as e:
        print(f"Bind failed. Error Code : {e}")
        sys.exit(1)

    s.setblocking(True)


def record(file_name: str, addr: tuple, buffer_size=65536, max_num_packets=1e9, max_seconds=1e9):
    """
    Records data from a specified address and saves it to a file or BytesIO object.

    Parameters:
        file_name (str): The name of the file to save the recorded data to.
        addr (tuple): The address to record data from.
        buffer_size (int, optional): The size of the buffer used for reading data. Defaults to 65536.
        max_num_packets (float, optional): The maximum number of packets to record. Defaults to 1e9.
        max_seconds (float, optional): The maximum number of seconds to record. Defaults to 1e9.

    Returns:
        None
    """
    signal.signal(signal.SIGINT, _signal_handler)
    with open_socket() as s:
        _prepare_socket(s, addr)
        if isinstance(file_name, BytesIO):
            _record_data(s, file_name, max_num_packets, max_seconds, buffer_size)
        else:
            with open(file_name, "wb") as f:
                _record_data(s, f, max_num_packets, max_seconds, buffer_size)


def main():
    """
    Parse inputs to start the recording of UPD packets

    :param server: Host to listen to (default: "127.0.0.1")
    :type server: str
    :param port: Port to listen to (default: 1234)
    :type port: int
    :param file: File to write data to (default: "udp.bin")
    :type file: str
    :param buffer: Host target (default: 65536)
    :type buffer: int
    :param count: Stop capture after x packets (default: 1000000000)
    :type count: int
    :param seconds: Stop capture after x seconds (default: 1000000000)
    :type seconds: int
    """
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
    record(
        file_name=args.file,
        addr=addr,
        buffer_size=args.buffer,
        max_num_packets=args.count,
        max_seconds=args.seconds,
    )


if __name__ == "__main__":
    main()
