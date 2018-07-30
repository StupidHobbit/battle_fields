from socket import socket
from typing import List, Tuple, AnyStr


Characters = List[dict]
Coord = Tuple[float, float]
ID = AnyStr


class GameClient(socket):
    def __init__(self, host: str, port: int):
        pass

    def auth(self, key: str):
        """
        Authorize with a given key
        """
        pass

    def info(self) -> dict:
        """
        Returns information about server
        """
        pass

    def add_character(self, character_class: str, name: str) -> ID:
        """
        Adds character with given attributes and returns his ID
        """
        pass

    def enter_game(self, character_id: ID):
        """
        Start a game with given character. After that messages from server can be accessed by get_message
        """
        pass

    def get_message(self) -> Characters:
        """
        Returns list of all visible characters. Character is described by dict.
        """
        pass

    def move(self, velocity: Coord):
        """
        Send command about changing player's direction of  movement
        """
        pass

    def message(self, text: str):
        """
        Post a message from player
        """
        pass

    def action(self, name: str, target_id: ID, coordinates: Coord):
        """
        Send command about making some action. Can be rejected
        """
        pass

    def sync(self):
        pass
