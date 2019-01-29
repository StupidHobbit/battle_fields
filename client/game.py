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
from utilities.spatial import Point
from client.character import Unit, Character
from client.config import *
from resources import CHARACTERS
from client.game_client import GameClient


MOVE_KEYS = {key.LEFT: Point(-1, 0), key.RIGHT: Point(1, 0),
             key.DOWN: Point(0, -1), key.UP: Point(0, 1)}


class Game():
    def proceed_packet(self, dt: float):
        units = self.game_client.get_message()
        if not units: return
        ping = time() - self.game_client.time_of_last_message
        t_units = {}
        #self.units.clear()
        for p in units:
            id = int(p['id'])
            new_dir = Point(float(p['dx']), float(p['dy']))
            new_pos = Point(float(p['x']), float(p['y'])) + new_dir * ping * 0.5
            unit = self.units.get(id)
            if unit:
                if new_dir != unit.dir:
                    unit.dir = new_dir
                if new_pos.distance(unit.pos) > MOVE_DIST:
                    unit.pos = new_pos
            else:
                arg = {'id': id, 'cls': p['cls'],
                       'pos': new_pos,
                       'dir': new_pos
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

    def __init__(self, window: pyglet.window.Window, game_client: GameClient):
        self.units = {}
        self.gui = Gui(window)
        self.camera = Camera(window)
        self.map = Map()
        self.game_client = game_client
        self.player_id = game_client.player_id
        window.move_keys_pressed = Point()
        clock.schedule_interval(self.update_units, TURN_DELAY)
        clock.schedule_interval(self.proceed_packet, PROCEED_DELAY / 2)

        @window.event
        def on_draw():
            window.clear()
            batch.draw()

        @window.event
        def on_key_press(symbol, modifiers):
            if symbol in MOVE_KEYS:
                window.move_keys_pressed += MOVE_KEYS[symbol]
                self.set_direction_of_player(window.move_keys_pressed)

        @window.event
        def on_key_release(symbol, modifiers):
            if symbol in MOVE_KEYS:
                window.move_keys_pressed -= MOVE_KEYS[symbol]
                self.set_direction_of_player(window.move_keys_pressed)

        @window.event
        def on_mouse_press(x, y, button, modifiers):
            pass

        @window.event
        def on_mouse_motion(x, y, dx, dy):
            pass

    def set_direction_of_player(self, dir: Point):
        if abs(dir):
            dir = dir / abs(dir) * self.units[self.player_id].speed
        print(dir)
        self.units[self.player_id].dir = dir
        self.game_client.move(dir)
