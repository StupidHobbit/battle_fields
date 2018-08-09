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

class Game():
    def procced_packet(self, dt: float):
        pass

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

        @window.event
        def on_draw():
            window.clear()
            batch.draw()

        @window.event
        def on_key_press(symbol, modifiers):
            if symbol == key.LEFT:
                self.units[self.player_id].dir = Point(-1, 0) * self.units[self.player_id].speed
                self.game_client.move(self.units[self.player_id].dir)
            elif symbol == key.RIGHT:
                self.units[self.player_id].dir = Point(1, 0) * self.units[self.player_id].speed
                self.game_client.move(self.units[self.player_id].dir)
            elif symbol == key.DOWN:
                self.units[self.player_id].dir = Point(0, 1) * self.units[self.player_id].speed
                self.game_client.move(self.units[self.player_id].dir)
            elif symbol == key.UP:
                self.units[self.player_id].dir = Point(0, -1) * self.units[self.player_id].speed
                self.game_client.move(self.units[self.player_id].dir)

        @window.event
        def on_mouse_press(x, y, button, modifiers):
            pass

        @window.event
        def on_mouse_motion(x, y, dx, dy):
            pass


