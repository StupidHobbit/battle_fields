import pyglet
from pyglet.gl import *

from client.gui import Gui
from client.map import Map


GUI_GROUP_NUM = 100


class Game():
    def __init__(self, window):
        self.units = {}
        self.player_id = -1
        self.batch = pyglet.graphics.Batch()
        self.gui_group = pyglet.graphics.OrderedGroup(GUI_GROUP_NUM)
        self.gui = Gui(window, self.batch, self.gui_group)
        self.map = Map(self.batch)

        @window.event
        def on_draw():
            window.clear()
            self.batch.draw()

## def