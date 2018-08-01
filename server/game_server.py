import socket
import threading
import socketserver
import json
from queue import Queue
from time import sleep


HOST, PORT = "localhost", 1488
PACKET_SIZE = 8096
SLEEP_TIME = 0.02


class GameHandler(socketserver.BaseRequestHandler):
    def handle(self):
        #try:
            while not self.server.closed:
                data = self.request.recv(PACKET_SIZE)
                if data:
                    data = json.loads(data.decode())
                    command = data.get('command')
                    ans = getattr(self, command, self.default)(data)
                    self.request.sendall(json.dumps(ans).encode())
                sleep(SLEEP_TIME)
        #finally:
        #    self.stop()

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
