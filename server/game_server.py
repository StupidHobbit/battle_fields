import socket
import asyncio
import threading
import socketserver
import json

from queue import Queue
from time import sleep


HOST, PORT = "localhost", 1488
PACKET_SIZE = 8096
SLEEP_TIME = 0.02


class GameHandler(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

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
        pass



class GameServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, incoming_queue, outcoming_queue, address=(HOST, PORT), handler=GameHandler):
        super().__init__(address, handler)
        self.incoming_queue = incoming_queue
        self.outcoming_queue = outcoming_queue
        self.closed = False

    def start(self):
        server_thread = threading.Thread(target=self.serve_forever)
        self.thread = server_thread
        # Exit the server thread when the main thread terminates
        #server_thread.daemon = True
        server_thread.start()

    def stop(self):
        print("Closing server...")
        self.closed = True
        self.shutdown()
        self.server_close()




class ServerException(Exception):
    """Base class for server exceptions"""
    pass
