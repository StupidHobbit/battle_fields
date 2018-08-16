import pyglet

import resources
from utilities import Point
from resources import UNITS_PIC
from client.render_manager import batch, units_group
from client.config import MOVE_DIST

class Unit:
    def __init__(self, id: int, cls: str, pos: Point, dir: Point):
        self.id = id
        self.cls = cls
        self._pos = pos
        self.dir = dir
        self.speed = 100
        self.sprite = pyglet.sprite.Sprite(
            UNITS_PIC[cls], x=pos.x, y=pos.y, batch=batch, group=units_group
        )

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos: Point):
        if pos.distance(self._pos) > MOVE_DIST:
            self._pos = pos
            self.sprite.update(pos.x, pos.y)

    def update(self, dt: float):
        self.pos = self.pos + self.dir * dt

class Character(Unit):
    def __init__(self, id: int, cls: str, pos: Point, dir: Point, name: str):
        Unit.__init__(self, id, cls, pos, dir)
        self.name = name
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