import pyglet
import resources

class Character:
    def __init__(self, class_name: str, nick_name: str, batch, group):
        self.class_name = class_name
        self.nick_name = nick_name
        pass

    def update(self, time: float):
        pass

    def set_data(self, coord):
        pass

    def action(self, action_name: str, dir):
        pass

    def reaction(self, reaction_name: str):
        pass

    def add_message(self, message: str):
        pass

    def set_effects(self, effects: list):
        pass

