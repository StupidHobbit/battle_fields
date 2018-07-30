import socket
import threading
import socketserver
import json
from queue import Queue
from time import sleep


HOST, PORT = "localhost", 1310
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
                    self.request.sendall(ans.encode())
                sleep(SLEEP_TIME)
        #finally:
        #    self.stop()

    def default(self, data):
        return json.dumps({"text": "Hello world", 'status': 200})

    def INFO(self):
        pass


class GameServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, queue, address=(HOST, PORT), handler=GameHandler):
        super().__init__(address, handler)
        self.queue = queue
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



if __name__ == '__main__':
    queue = Queue()
    server = GameServer(queue)
    server.start()
    ip, port = server.server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    data = json.dumps({"command": "PING"})
    sock.sendall(data.encode())
    ans = json.loads(sock.recv(1024).decode())
    print(ans)
    sock.close()
    server.stop()
