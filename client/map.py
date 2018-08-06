import pyglet

from utilities.resources import tiled_map
from client.render_manager import batch


class Map:
    def __init__(self):
        self.groups = []
        tilewidth, tileheight = tiled_map.tilewidth, tiled_map.tileheight
        height = tiled_map.height - 1
        for i, layer in enumerate(tiled_map.layers):
            group = pyglet.graphics.OrderedGroup(i)
            sprites = [
                pyglet.sprite.Sprite(img=image, x=x * tilewidth, y=(height - y) * tileheight, batch=batch, group=group)
                for x, y, image in layer.tiles()
                ]
            self.groups.append((group, sprites))