import asyncio
import json
from random import randint
from multiprocessing.dummy import Pool
from time import sleep, perf_counter as time

import redis

from resources import MAP_HEIGHT, MAP_WIDTH
from server.config import REDIS_SOCKET_PATH, VIEW_RADIUS
from utilities.sphere_coords import get_lon_lat


HOST, PORT = "localhost", 1488
PACKET_SIZE = 8096
SLEEP_TIME = 0.02


class GameHandler(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {peername}')
        self.transport = transport
        self.r = redis.Redis(unix_socket_path=REDIS_SOCKET_PATH, decode_responses=True)
        self.pool = Pool(5)
        self.id = 0
        self.unit_name = ''

    def data_received(self, data):
        message = json.loads(data.decode())
        #print('Data received: {!r}'.format(message))
        command = message.get('command')

        ans = getattr(self, command, self.default)(message)
        message = json.dumps(ans)
        self.transport.write(message.encode())
        print('Send: {!r}'.format(message))

    def default(self, data):
        return {"text": "Hello world", 'status': 200}

    def TIME(self, data):
        return {'time': time()}

    def INFO(self, data):
        return {"players": self.r.get('players'), 'status': 200}

    def AUTH(self, data):
        return {'status': 200}

    def ADCH(self, data):
        id = self.r.incr('next_id')
        name = data['name']
        if self.r.sismember('names', name):
            return {'status': 300}
        self.r.sadd('names', name)
        char_name = 'char' + str(id)
        self.r.hmset(char_name, {'name': name, 'cls': data['cls']})
        return {'id': id, 'status': 200}

    def ENGM(self, data):
        id = data['id']
        unit_name = 'unit'+str(id)
        if self.r.exists(unit_name):
           return {'status': 300}
        char = self.r.hgetall('char'+str(id))
        if not char:
            return {"status": 400}
        self.id = id
        self.unit_name = unit_name
        x, y = randint(0, MAP_WIDTH-1), randint(0, MAP_HEIGHT-1)
        char['x'], char['y'] = x, y
        char['id'] = id
        char['hp'] = 10
        self.r.geoadd('map', *get_lon_lat(x, y), self.id)
        char['dx'], char['dy'] = 0, 0
        self.r.hmset(unit_name, char)
        self.r.publish('new_units', unit_name)
        return {'status': 200}

    def MOVE(self, data):
        if not self.id: return
        unit = list(map(float, self.r.hmget(self.unit_name, ('x', 'y', 'dx', 'dy'))))
        ping = time() - data['time']
        dx, dy = data['dx'], data['dy']
        x = unit[0] + (dx - unit[2]) * ping
        y = unit[1] + (dy - unit[3]) * ping
        self.r.hmset(self.unit_name, {'x': x, 'y': y, 'dx': dx, 'dy': dy})
        return {}

    def NEXT(self, data):
        if not self.id: return
        chars_id = self.r.georadiusbymember('map', self.id, VIEW_RADIUS)
        chars_bd_names = ['unit' + s for s in chars_id]
        res = self.pool.map(self.r.hgetall, chars_bd_names)
        return res, time()

    def connection_lost(self, exc):
        if not self.id: return
        self.r.publish('deleted_units', self.unit_name)


class ServerException(Exception):
    """Base class for server exceptions"""
    pass
