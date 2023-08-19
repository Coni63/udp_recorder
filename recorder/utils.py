from __future__ import annotations

import socket
from contextlib import contextmanager


@contextmanager
def open_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Socket created")
        yield s
    except OSError as msg:
        print("Failed to create socket")
        print(f"Message : {msg}")
    finally:
        s.close()
