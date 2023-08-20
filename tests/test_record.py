from __future__ import annotations

import pickle
import socket
import threading
import time
import unittest
from io import BytesIO

from udprecorder.record_udp_stream import record


class TestRecord(unittest.TestCase):
    def setUp(self):
        self.emitter = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = ("127.0.0.1", 12345)
        self.msg_list = [b"123", b"4567"]

    def tearDown(self):
        self.emitter.close()

    def test_record(self):
        """
        Create in a separated Thread a socket to emit messages
        Use the recorder to save it and validate the saved result
        """

        def emitter():
            for msg in self.msg_list:
                time.sleep(0.1)
                self.emitter.sendto(msg, self.addr)

        threading.Thread(target=emitter).start()

        fake_file = BytesIO()
        record(fake_file, self.addr, max_num_packets=len(self.msg_list))
        fake_file.seek(0)

        self.assertEqual(fake_file.getbuffer().nbytes, 59)

        for msg_sent in self.msg_list:
            elapsed_time, msg_received = pickle.load(fake_file)
            self.assertEqual(msg_received, msg_sent)
            self.assertAlmostEqual(elapsed_time, 0.1, 1)

        with self.assertRaises(EOFError):
            pickle.load(fake_file)
