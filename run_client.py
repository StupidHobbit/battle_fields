import pyglet

from client.game import Game


window = pyglet.window.Window()
game = Game(window)
pyglet.app.run()
