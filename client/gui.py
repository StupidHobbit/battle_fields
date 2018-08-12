import pyglet
import glooey

from client.render_manager import batch, gui_group as group


class Gui(glooey.Gui):
    def __init__(self, window):
        super().__init__(window, batch, group)
