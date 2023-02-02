import random

from SnakeLogic import SnakeLogic


class RandomSearch(SnakeLogic):
    def __init__(self):
        super().__init__("Random Search")
        self.reset()

    def move(self):
        potential_steps = [[self.body[0][0] + 1, self.body[0][1]], [self.body[0][0] - 1, self.body[0][1]],
                           [self.body[0][0], self.body[0][1] + 1], [self.body[0][0], self.body[0][1] - 1]]

        step = potential_steps[random.randint(0,3)]
        self.body.insert(0, step)

        self.checkAte()
        return step
