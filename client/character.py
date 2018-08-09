import pyglet
import resources
from utilities import Point


class Unit:
    def __init__(self, id: int, name: str, pos: Point, dir: Point):
        self.id = id
        self.name = name
        self.pos = pos
        self.dir = dir
        self.speed = 2

    def update(self, dt: float):
        self.pos += self.dir * dt

class Character(Unit):
    def __init__(self, id: int, name: str, pos: Point, dir: Point, nick: str):
        Unit.__init__(self, id, name, pos, dir)
        self.nick = nick
        self.max_hp = 2 # Will load
        self.hp = self.max_hp

    def action(self, name: str, dir: Point):
        pass

    def reaction(self, name: str):
        pass

    def add_message(self, msg: str):
        pass

    def set_effects(self, effect: list):
        pass

