from random import random

import pyglet
pyglet.options['debug_gl'] = False

from client.game import Game
from client.game_client import GameClient
from client.config import HOST, PORT


client = GameClient(HOST, PORT)
client.auth('123')
id = client.add_character(name=str(random()), cls='warrior')
client.enter_game(id)

window = pyglet.window.Window(fullscreen=False, width = 1024, height = 700)
game = Game(window, client)

pyglet.app.run()
