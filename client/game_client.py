import json
import socket
from typing import List, Tuple, AnyStr
import _thread
from time import time, sleep

from utilities import Point
from client.config import PROCCED_DELAY, MOVE_DELAY

Characters = List[dict]
Coord = Tuple[float, float]
ID = AnyStr


class Error(Exception):
    """Base class for exceptions in this module.
    Attributes:
        status -- status, returned by server
        message -- explanation of the error
    """

    def __init__(self, status, message=''):
        self.status = status
        self.message = message

class AuthorizationError(Error):
    pass

class AddCharacterError(Error):
    pass

class EnterGameError(Error):
    pass


class GameClient():
    def __init__(self, host: str, port: int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.lock = _thread.allocate_lock()
        self.is_receiving_messages = False
        self.units = []
        #self.move_thread = _thread.start_new_thread()
        self.next_move = None
        self.is_sending_moves = False

    def __del__(self):
        self.sock.close()

    def send_request(self, command, back=True, **kwargs):
        kwargs['command'] = command
        data = json.dumps(kwargs)
        with self.lock:
            self.sock.sendall(data.encode())
            ans = json.loads(self.sock.recv(1024).decode())
        return ans

    def auth(self, key: str):
        """
        Authorize with a given key
        """
        ans = self.send_request('AUTH', key=key)
        if ans['status'] != 200:
            raise AuthorizationError(ans['status'])

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
        else:
            raise AddCharacterError(ans['status'])

    def enter_game(self, character_id: ID):
        """
        Start a game with given character. After that messages from server can be accessed by get_message
        """
        ans = self.send_request('ENGM', id=character_id)
        self.player_id = character_id
        self.start_receiving_messages()
        self.start_sending_moves()
        if ans['status'] != 200:
            raise AuthorizationError(ans['status'])

    def move(self, point: Point):
        """
        Send command about changing player's direction of  movement
        """
        self.next_move = point

    def start_sending_moves(self):
        _thread.start_new_thread(self.do_sending_moves(), ())

    def do_sending_moves(self):
        self.is_sending_moves = True
        while self.is_sending_moves:
            if not self.next_move is None:
                point = self.next_move
                self.next_move = None
                last_time = time()
                self.send_request('MOVE', dx=point.x, dy=point.y)
                sleep(max(MOVE_DELAY - time() + last_time, 0))
        _thread.exit_thread()

    def stop_sending_moves(self):
        self.is_sending_moves = False

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

    def get_message(self) -> Characters:
        """
        Returns list of all visible characters. Character is described by dict.
        """
        return self.units

    def start_receiving_messages(self):
        _thread.start_new_thread(self.do_receiving_messages, ())

    def do_receiving_messages(self):
        self.is_receiving_messages = True
        while self.is_receiving_messages:
            last_time = time()
            self.units = self.send_request('NEXT')
            sleep(max(PROCCED_DELAY - time() + last_time, 0))
        _thread.exit_thread()

    def stop_receiving_messages(self):
        self.is_receiving_messages = False

    def sync(self):
        pass
