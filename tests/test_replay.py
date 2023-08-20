from __future__ import annotations

import pickle
import unittest
from io import BytesIO
from unittest.mock import patch

from udprecorder.replay_udp_stream import replay


class TestRecord(unittest.TestCase):
    def setUp(self):
        self.addr = ("127.0.0.1", 12345)
        self.msg_list = [b"123", b"4567"]

    def test_record(self):
        """
        Create a fake save and run it by mocking the method to emit the signal
        Simply check that the method is called the proper number of times
        """
        fake_file = BytesIO()
        for msg in self.msg_list:
            pickle.dump((0.1, msg), fake_file)
        fake_file.seek(0)

        with patch("socket.socket.sendto") as sender_mock:
            sender_mock.return_value = 1
            replay(fake_file, self.addr)
            self.assertEqual(sender_mock.call_count, len(self.msg_list))
