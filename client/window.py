import pyglet

from gui import Gui


class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super.__init__(self, *args, **kwargs)
        self.units = {}
        self.player_id = -1
        self.batch = pyglet.graphics.Batch()
        self.groups = []
        gui_group = pyglet.graphics.OrderedGroup()
        self.gui = Gui()
