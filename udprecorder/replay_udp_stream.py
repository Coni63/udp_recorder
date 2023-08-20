from __future__ import annotations

import argparse
import pickle
import socket
import time
from io import BufferedReader
from io import BytesIO

from .utils import open_socket


def _replay_data(s: socket.socket, data: BytesIO | BufferedReader, addr: tuple):
    """
    Replays data received to a socket to a specified address.

    Parameters:
        s (socket.socket): The socket object used for sending data.
        data (BytesIO | BufferedReader): The data stream to replay.
        addr (tuple): The address to send the data to.

    Returns:
        None
    """
    print("Start the replay")
    while True:
        try:
            time_until_msg, msg = pickle.load(data)
            time.sleep(time_until_msg)
            s.sendto(msg, addr)
        except (EOFError, pickle.UnpicklingError):
            print("End of file reached")
            break
        except Exception as e:
            print(f"Event failed with error '{e}'")
            pass


def replay(file_name: str, addr: tuple):
    """
    Replays data from a file or BytesIO object to a specified address.

    Parameters:
        file_name (str): The name of the file to replay data from. If a BytesIO
            object is provided, the data will be read from it instead.
        addr (tuple): The address to replay the data to.

    Returns:
        None
    """
    with open_socket() as s:
        if isinstance(file_name, BytesIO):
            _replay_data(s, file_name, addr)
        else:
            with open(file_name, "rb") as f:
                _replay_data(s, f, addr)


def main():
    """
    This function is the entry point of the program to replay a saved stream

    It parses command line arguments and sends a UDP file captured previously using record_udp_stream.py.

    Parameters:
        None

    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="Replay UDP stream from a file captured previously using the recorder",
    )
    parser.add_argument("-s", "--server", help="Host target", required=False, type=str, default="127.0.0.1")
    parser.add_argument("-p", "--port", help="Port to listen", required=False, type=int, default=1234)
    parser.add_argument("-f", "--file", help="File to send", required=False, type=str, default="udp.bin")

    args = parser.parse_args()

    addr = (args.server, args.port)
    replay(args.file, addr)


if __name__ == "__main__":
    main()
