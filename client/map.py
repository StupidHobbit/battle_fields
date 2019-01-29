import pyglet

from resources import tiled_map
from client.render_manager import batch


class Map:
    def __init__(self):
        self.groups = []
        tilewidth, tileheight = tiled_map.tilewidth, tiled_map.tileheight
        height = tiled_map.height - 1
        layer_level_correction = 0
        for i, layer in enumerate(tiled_map.layers):
            if layer.name == "units":
                layer_level_correction = 6 - i
                continue
            if layer.name == "obstacles":
                continue
            group = pyglet.graphics.OrderedGroup(i + layer_level_correction)
            sprites = [
                pyglet.sprite.Sprite(img=image, x=x * tilewidth, y=(height - y) * tileheight, batch=batch, group=group)
                for x, y, image in layer.tiles()
                ]
            self.groups.append((group, sprites))
