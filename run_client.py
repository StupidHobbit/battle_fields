import pyglet
pyglet.options['debug_gl'] = False

from client.game import Game


window = pyglet.window.Window(fullscreen=True)
game = Game(window)
pyglet.app.run()
