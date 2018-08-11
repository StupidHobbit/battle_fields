from pytmx.util_pyglet import load_pyglet
import pyglet
from os import path


tiled_map = load_pyglet('resources/map.tmx')
MAP_WIDTH = tiled_map.width * tiled_map.tilewidth
MAP_HEIGHT = tiled_map.height * tiled_map.tileheight
CHARACTERS = {'warrior'}
UNITS_PIC = {}

for name in CHARACTERS:
    UNITS_PIC[name] = pyglet.image.load(path.join("resources", name + '.png'))