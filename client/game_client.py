import json
import socket
from typing import List, Tuple, AnyStr


Characters = List[dict]
Coord = Tuple[float, float]
ID = AnyStr


class GameClient():
    def __init__(self, host: str, port: int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def __del__(self):
        self.sock.close()

    def send_request(self, command, **kwargs):
        kwargs['command'] = command
        data = json.dumps(kwargs)
        self.sock.sendall(data.encode())
        data = self.sock.recv(1024)
        if data:
            return json.loads(data.decode())

    def auth(self, key: str):
        """
        Authorize with a given key
        """
        ans = self.send_request('AUTH', key=key)
        return ans['status'] == 200

    def info(self) -> dict:
        """
        Returns information about server
        """
        return self.send_request('INFO')

    def add_character(self, cls: str, name: str) -> ID:
        """
        Adds character with given attributes and returns his ID
        """
        ans = self.send_request('ADCH', cls=cls, name=name)
        if ans['status'] == 200:
            return ans['id']

    def enter_game(self, character_id: ID):
        """
        Start a game with given character. After that messages from server can be accessed by get_message
        """
        ans = self.send_request('ENGM', id=character_id)
        return ans['status'] == 200

    def get_message(self) -> Characters:
        """
        Returns list of all visible characters. Character is described by dict.
        """
        return self.send_request('NEXT')['characters']

    def move(self, velocity: Coord):
        """
        Send command about changing player's direction of  movement
        """
        self.send_request('MOVE', velocity=velocity)

    def message(self, text: str):
        """
        Post a message from player
        """
        self.send_request('MESG', text=text)

    def action(self, name: str, id: ID, coord: Coord):
        """
        Send command about making some action. Can be rejected
        """
        self.send_request('ACTN', name=name, id=id, coord=coord)

    def sync(self):
        pass
