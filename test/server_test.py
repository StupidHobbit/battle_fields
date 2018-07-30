import unittest
import socket
import json
from queue import Queue
from server.game_server import *


class TestServerMethods(unittest.TestCase):
    def setUp(self):
        queue = Queue()
        server = GameServer(queue)
        self.server = server
        self.queue = queue
        server.start()
        ip, port = server.server_address
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        self.sock = sock

    def test_connection(self):
        data = json.dumps({"command": "PING"})
        self.sock.sendall(data.encode())
        ans = json.loads(self.sock.recv(1024).decode())
        self.assertIn("text", ans, "Wrong format returned")
        self.assertEqual(ans["text"], "Hello world")

    def tearDown(self):
        self.server.stop()
        self.sock.close()


if __name__ == '__main__':
    unittest.main()