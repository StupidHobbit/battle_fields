import pyglet
from pyglet.gl import *

from client.gui import Gui
from client.map import Map
from client.camera import Camera
from client.render_manager import batch
from client.config import *
from client.camera import Camera


class Game():
    def procced_packet(self, dt: float):
        pass

    def send_message(self, msg: str):
        pass

    def start_action(self, name: str):
        pass

    def __init__(self, window):
        self.units = {}
        self.player_id = -1
        self.gui = Gui(window)
        self.camera = Camera(window)
        self.map = Map()

        @window.event
        def on_draw():
            window.clear()
            batch.draw()

        @window.event
        def on_key_press(symbol, modifiers):
            pass

        @window.event
        def on_mouse_press(x, y, button, modifiers):
            pass

        @window.event
        def on_mouse_motion(x, y, dx, dy):
            pass


