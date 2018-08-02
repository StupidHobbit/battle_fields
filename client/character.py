import pyglet
import resources
from utilities import Point


class Unit:
    def __init__(self, name: str, pos: Point=Point(0, 0)):
        self.name = name
        self.pos = pos
        self.v = Point(2, 2)

    def update(self, dt: float):
        self.pos = self.v * dt

class Character(Unit):
    def __init__(self, name: str, nick: str, batch, group, pos: Point=Point(0, 0)):
        Unit.__init__(self, name, pos)
        self.nick = nick
        self.batch = batch
        self.group = group
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

