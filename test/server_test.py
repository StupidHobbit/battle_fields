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

    def send_request(self, command, **kwargs):
        kwargs['command'] = command
        data = json.dumps(kwargs)
        self.sock.sendall(data.encode())
        return json.loads(self.sock.recv(1024).decode())

    def test_connection(self):
        ans = self.send_request('PING')
        self.assertIn("text", ans, "Wrong format returned")
        self.assertEqual(ans["text"], "Hello world")

    def test_info(self):
        ans = self.send_request('INFO')
        self.assertIn("players", ans, "Wrong format returned")
        players = ans["players"]


    def test_auth(self):
        ans = self.send_request('AUTH', key='123')
        self.assertIn("status", ans, "Wrong format returned")
        self.assertEqual(ans["status"], 200)

    def test_adch(self):
        ans = self.send_request('ADCH', name='Bill', cls='warrior')
        self.assertIn("id", ans, "Wrong format returned")
        id = ans["id"]
        ans = self.send_request('ADCH', name='Bill', cls='warrior')
        self.assertNotEqual(ans["id"], id, "Same id returned")



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