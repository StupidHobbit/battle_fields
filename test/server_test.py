import unittest
import socket
import json
import redis
from timeit import timeit


HOST, PORT = "localhost", 1488


class TestServerMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        cls.sock = sock

    def test_connection(self):
        data = json.dumps({"command": "PING"})
        self.sock.sendall(data.encode())
        ans = json.loads(self.sock.recv(1024).decode())
        self.assertIn("text", ans, "Wrong format returned")
        self.assertEqual(ans["text"], "Hello world")

    def test_info(self):
        data = json.dumps({"command": "INFO"})
        self.sock.sendall(data.encode())
        ans = json.loads(self.sock.recv(1024).decode())
        self.assertIn("players", ans, "Wrong format returned")
        self.assertEqual(ans["players"], 666)

    def test_auth(self):
        data = json.dumps({"command": "AUTH", "key": "1234"})
        self.sock.sendall(data.encode())
        ans = json.loads(self.sock.recv(1024).decode())
        self.assertIn("status", ans, "Wrong format returned")
        self.assertEqual(ans["status"], 200)

    @classmethod
    def tearDownClass(cls):
        cls.sock.close()


class TestRedisPerfomance(unittest.TestCase):
    def test_units(self):
        r = redis.Redis(unix_socket_path='/tmp/redis.sock')
        r.hmset("unit1", {'x': 100, 'y': 200, 'hp': 10})
        for i in range(10000):
            x, y, hp = map(int, r.hvals("unit1"))
            x += 1
            y += 1
            hp += 1
            r.hmset("unit1", {'x': x, 'y': y, 'hp': hp})


if __name__ == '__main__':
    unittest.main()