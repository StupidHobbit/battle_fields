import pyglet
from pyglet.gl import *

from utilities.spatial import Point


class Camera:
    def __init__(self, window):
        self.position = Point(0, 0)
        self._zoom = 1
        self.size = Point(window.width, window.height)
        self.window = window

    @property
    def center(self):
        return self.position + self.size // 2

    @center.setter
    def set_senter(self, center):
        pass

    def move(self, delta):
        pass

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def set_zoom(self, zoom):
        pass

    def get_global_coordinates(self, point):
        pass