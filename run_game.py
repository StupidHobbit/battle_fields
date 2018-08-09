from server.game import Game


game = Game()
# Serve requests until Ctrl+C is pressed
try:
    game.run_forever()
except KeyboardInterrupt:
    pass

# Close the game
game.shutdown()
