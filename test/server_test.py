import unittest
import json
import redis
if __name__ == '__main__':
    import sys
    sys.path.append('./')
from client.game_client import GameClient
from utilities import Point
from server.config import REDIS_SOCKET_PATH
from timeit import timeit


HOST, PORT = "localhost", 1488


class TestServerMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game_client = GameClient(HOST, PORT)

    def test_connection(self):
        ans = self.game_client.send_request('PING')
        self.assertIn("text", ans, "Wrong format returned")
        self.assertEqual(ans["text"], "Hello world")

    def test_info(self):
        ans = self.game_client.info()
        self.assertIn("players", ans, "Wrong format returned")
        players = ans["players"]

    def test_auth(self):
        ans = self.game_client.auth(key='123')
        self.assertEqual(ans, True)

    def test_adch(self):
        id1 = self.game_client.add_character(name='Bill', cls='warrior')
        id2 = self.game_client.add_character(name='Ann', cls='warrior')
        self.assertNotEqual(id1, id2, "Same id returned")

    def test_move(self):
        id = self.game_client.add_character(name='Dad', cls='warrior')
        self.game_client.enter_game(id)
        self.game_client.move(Point(1, 2))
        r = redis.Redis(unix_socket_path=REDIS_SOCKET_PATH)
        dad = r.hgetall(b'unit'+bytes(id))
        self.assertEqual((dad['dx'], dad['dy']), (1, 2))



    @classmethod
    def tearDownClass(cls):
        pass


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