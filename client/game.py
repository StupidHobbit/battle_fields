import pyglet
from pyglet.gl import *

from client.gui import Gui
from client.map import Map
from client.render_manager import batch
from client.config import *
from client.camera import Camera


class Game():
    def update_from_server(self, dt):
        pass

    def __init__(self, window):
        self.units = {}
        self.player_id = -1
        self.gui = Gui(window)
        self.map = Map()

        @window.event
        def on_draw():
            window.clear()
            batch.draw()

## def
