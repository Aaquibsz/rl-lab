import random


class RandomAgent:

    def __init__(self):
        self.actions = [
            "UP",
            "DOWN",
            "LEFT",
            "RIGHT"
        ]

    def choose_action(self, state):
        return random.choice(self.actions)