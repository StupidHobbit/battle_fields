import socket
import asyncio
import json
from random import randint
from multiprocessing.dummy import Pool

import redis

from utilities.resources import MAP_HEIGHT, MAP_WIDTH
from server.config import REDIS_SOCKET_PATH, VIEW_RADIUS
from utilities.sphere_coords import get_lon_lat


HOST, PORT = "localhost", 1488
PACKET_SIZE = 8096
SLEEP_TIME = 0.02


class GameHandler(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        self.r = redis.Redis(unix_socket_path=REDIS_SOCKET_PATH)

    def data_received(self, data):
        message = json.loads(data.decode())
        print('Data received: {!r}'.format(message))
        command = message.get('command', '')

        ans = getattr(self, command, self.default)(message)
        if ans:
            message = json.dumps(ans)
            print('Send: {!r}'.format(message))
            self.transport.write(message.encode())

    def default(self, data):
        return {"text": "Hello world", 'status': 200}

    def INFO(self, data):
        return {"players": self.r.get('players').decode(), 'status': 200}

    def AUTH(self, data):
        return {'status': 200}

    def ADCH(self, data):
        id = self.r.incr('next_id')
        if self.r.sismember('names', data['name']):
            return {'status': 300}
        char_name = b'char' + bytes(id)

        self.r.hmset(char_name, {'name': data['name'], 'cls': data['cls']})
        return {'id': id, 'status': 200}

    def ENGM(self, data):
        id = data['id']
        unit_name = b'unit'+bytes(id)
        if self.r.exists(unit_name):
           return {'status': 300}
        char = self.r.hgetall(b'char'+bytes(id))
        if not char:
            return {"status": 400}
        self.id = id
        self.unit_name = unit_name
        x, y = randint(0, MAP_WIDTH-1), randint(0, MAP_HEIGHT-1)
        char[b'x'], char[b'y'] = x, y
        self.r.geoadd('map', *get_lon_lat(x, y), self.id)
        char[b'dx'], char[b'dy'] = 0, 0
        self.r.hmset(unit_name, char)
        return {'status': 200}

    def MOVE(self, data):
        self.r.hmset(self.unit_name, {'dx': data['dx'], 'dy': data['dy']})

    def NEXT(self, data):
        chars_id = self.r.georadiusbymember('map', self.id, VIEW_RADIUS)
        print(chars_id)
        pool = Pool(5)
        #pool.map()



class ServerException(Exception):
    """Base class for server exceptions"""
    pass
