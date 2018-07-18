from socket import socket
from typing import List, Tuple


Characters = List[dict]
Coord = Tuple[float, float]

class GameClient(socket):
    def __init__(self, host: str, port: int):
        pass

    def auth(self, key: str):
        pass

    def info(self) -> dict:
        pass

    def add_character(self, character_class: str, name: str) -> str:
        pass

    def enter_game(self, character_id: str):
        pass

    def get_message(self) -> Characters:
        pass

    def move(self, velocity: Coord):
        pass

    def message(self, text: str):
        pass

    def action(self, name: str, target_id: str, coordinates: Coord, direction: float):
        pass

    def sync(self):
        pass