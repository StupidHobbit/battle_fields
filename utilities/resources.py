from pytmx.util_pyglet import load_pyglet


tiled_map = load_pyglet('resources/map.tmx')
MAP_WIDTH = tiled_map.width * tiled_map.tilewidth
MAP_HEIGHT = tiled_map.height * tiled_map.tileheight
