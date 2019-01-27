from time import time, sleep

import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet import clock


from client.gui import Gui
from client.map import Map
from client.camera import Camera
from client.render_manager import batch
from client.camera import Camera
from utilities import Point
from client.character import Unit, Character
from client.config import *
from resources import CHARACTERS


MOVE_KEYS = {key.LEFT: Point(-1, 0), key.RIGHT: Point(1, 0),
             key.DOWN: Point(0, -1), key.UP: Point(0, 1)}


class Game():
    def proceed_packet(self, dt: float):
        units = self.game_client.get_message()
        if not units: return
        t_units = {}
        #self.units.clear()
        for p in units:
            id = int(p['id'])
            if id in self.units:
                unit = self.units[id]
                new_pos = Point(float(p['x']), float(p['y']))
                new_dir = Point(float(p['dx']), float(p['dy']))
                if new_pos.distance(unit.pos) > MOVE_DIST:
                    unit.pos = new_pos
                unit.dir = new_dir
            else:
                arg = {'id': id, 'cls': p['cls'],
                       'pos': Point(float(p['x']), float(p['y'])),
                       'dir': Point(float(p['dx']), float(p['dy']))
                       }
                if p['cls'] in CHARACTERS:
                    arg['name'] = p['name']
                    unit = Character(**arg)
                else:
                    unit = Unit(**arg)
            if p['cls'] in CHARACTERS:
                unit.hp = p['hp']
            t_units[id] = unit
        self.units = t_units

    def update_units(self, dt: float):
        for unit in self.units.values():
            unit.update(dt)

    def send_message(self, msg: str):
        pass

    def start_action(self, name: str):
        pass

    def __init__(self, window, game_client):
        self.units = {}
        self.gui = Gui(window)
        self.camera = Camera(window)
        self.map = Map()
        self.game_client = game_client
        self.player_id = game_client.player_id
        clock.schedule_interval(self.update_units, TURN_DELAY)
        clock.schedule_interval(self.proceed_packet, PROCEED_DELAY / 2)

        @window.event
        def on_draw():
            window.clear()
            batch.draw()

        @window.event
        def on_key_press(symbol, modifiers):
            if symbol in MOVE_KEYS:
                print(self.units)
                self.units[self.player_id].dir = MOVE_KEYS[symbol] * self.units[self.player_id].speed
                self.game_client.move(self.units[self.player_id].dir)

        @window.event
        def on_key_release(symbol, modifiers):
            if symbol in MOVE_KEYS:
                print(self.units)
                self.units[self.player_id].dir = Point(0, 0)
                self.game_client.move(self.units[self.player_id].dir)

        @window.event
        def on_mouse_press(x, y, button, modifiers):
            pass

        @window.event
        def on_mouse_motion(x, y, dx, dy):
            pass


