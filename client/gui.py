import pyglet
import glooey

from client.render_manager import batch, gui_group as group


class Gui(glooey.Gui):
    def __init__(self, window):
        super().__init__(window, batch, group)
        vbox = glooey.VBox()
        vbox.alignment = 'center'
        self.vbox = vbox
        label = glooey.Label("Hello world")
        label.custom_color = '#000000'
        vbox.add(label)
        self.add(vbox)