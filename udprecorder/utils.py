from __future__ import annotations

import socket
from contextlib import contextmanager


@contextmanager
def open_socket():
    """
    A context manager that opens a socket.

    This function creates a socket using the socket.AF_INET and socket.SOCK_DGRAM parameters.
    It prints "Socket created" to indicate that the socket was successfully created.

    Parameters:
    None

    Returns:
    - s (socket): The created socket object.

    Raises:
    - OSError: If the socket creation fails, an OSError is raised.

    Examples:
    Usage example 1:
    with open_socket() as s:
        # Do something with the socket

    Usage example 2:
    try:
        with open_socket() as s:
            # Do something with the socket
    except OSError as e:
        # Handle the exception

    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Socket created")
        yield s
    except OSError as msg:
        print("Failed to create socket")
        print(f"Message : {msg}")
    finally:
        s.close()
