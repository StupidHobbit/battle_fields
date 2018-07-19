import pyglet

from client.gui import Gui


GUI_GROUP_NUM = 100


class Game():
    def __init__(self, window):
        self.units = {}
        self.player_id = -1
        self.batch = pyglet.graphics.Batch()
        self.groups = []
        gui_group = pyglet.graphics.OrderedGroup(GUI_GROUP_NUM)
        self.gui = Gui(window, self.batch, gui_group)
