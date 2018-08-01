from queue import Queue
from server.game_server import GameServer
import socket
import json


class Game:
    def __init__(self):
        self.incoming_queue = Queue()
        self.outcoming_queue = Queue()
        server = GameServer(self.incoming_queue, self.outcoming_queue)
        server.start()
        self.server = server
        self.units = {}
        self.characters = {}

    def shutdown(self):
        self.server.stop()


if __name__ == '__main__':
    game = Game()
    ip, port = game.server.server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    data = json.dumps({"command": "PING"})
    sock.sendall(data.encode())
    ans = json.loads(sock.recv(1024).decode())
    print(ans)
    sock.close()
    game.shutdown()
