import pyglet
import glooey


class Gui(glooey.Gui):
    def __init__(self, window, batch, group):
        super().__init__(window, batch, group)
