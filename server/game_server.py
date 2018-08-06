import socket
import asyncio
import threading
import socketserver
import json

import redis

from queue import Queue
from time import sleep
from server.config import REDIS_SOCKET_PATH


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
        message = json.dumps(ans)
        print('Send: {!r}'.format(message))
        self.transport.write(message.encode())

    def default(self, data):
        return {"text": "Hello world", 'status': 200}

    def INFO(self, data):
        return {"players": 666, 'status': 200}

    def AUTH(self, data):
        return {'status': 200}

    def ADCH(self, data):
        id = self.r.incr('players')
        self.r.hmset(b'char'+bytes(id), {'name': data['name'], 'cls': data['cls']})
        return {'id': id, 'status': 200}

    def ENGM(self, data):
        return {'status': 200}


class ServerException(Exception):
    """Base class for server exceptions"""
    pass
