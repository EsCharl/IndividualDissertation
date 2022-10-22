import random

from SnakeLogic import SnakeLogic


class RandomSearch(SnakeLogic):
    def __init__(self):
        self.reset()

    def move(self):
        potential_steps = []

        potential_steps.append([self.body[0][0] + 1, self.body[0][1]])
        potential_steps.append([self.body[0][0] - 1, self.body[0][1]])
        potential_steps.append([self.body[0][0], self.body[0][1] + 1])
        potential_steps.append([self.body[0][0], self.body[0][1] - 1])

        self.body.insert(0, potential_steps[random.randint(0,3)])

        self.checkAte()
        return self.body
