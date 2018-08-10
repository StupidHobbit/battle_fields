import pyglet
from pyglet.gl import *
from pyglet.window import key
from client.gui import Gui
from client.map import Map
from client.camera import Camera
from client.render_manager import batch
from client.config import *
from client.camera import Camera
from client.game_client import GameClient
from utilities import Point
from client.character import Unit, Character
from pyglet import clock
from config import *


MOVE_KEYS = {key.LEFT: Point(-1, 0), key.RIGHT: Point(1, 0),
             key.DOWN: Point(0, -1), key.UP: Point(0, 1)}


class Game():
    def procced_packet(self, dt: float):
        units = self.game_client.get_message()
        self.units.clear()
        for p in units:
            arg = {'id': int(p['id']), 'name': p['name'],
                   'pos': Point(int(p['x']), int(p['y'])),
                   'dir': Point(int(p['dx']), int(p['dy']))
                   }
            if p['name'] in CHARACTERS:
                arg += {'nick': p['nick']}
                unit = Character(**arg)
                unit.hp = int(p['hp'])
            else:
                unit = Unit(**arg)
            self.units[p['id']] = unit

    def update_units(self, dt: float):
        map(Unit.update, self.units.values())

    def send_message(self, msg: str):
        pass

    def start_action(self, name: str):
        pass

    def __init__(self, window, game_client, host: str, port: int):
        self.units = {}
        self.gui = Gui(window)
        self.camera = Camera(window)
        self.map = Map()
        self.game_client = game_client
        self.player_id = game_client.player_id
        clock.schedule_interval(self.update_units, TURN_DELAY)
        clock.schedule_interval(self.procced_packet, PROCCED_DELAY)

        @window.event
        def on_draw():
            window.clear()
            batch.draw()

        @window.event
        def on_key_press(symbol, modifiers):
            if symbol in MOVE_KEYS:
                self.units[self.player_id].dir = MOVE_KEYS[symbol] * self.units[self.player_id].speed
                self.game_client.move(self.units[self.player_id].dir)

        @window.event
        def on_mouse_press(x, y, button, modifiers):
            pass

        @window.event
        def on_mouse_motion(x, y, dx, dy):
            pass


