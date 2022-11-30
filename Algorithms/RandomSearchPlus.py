import random

from Constants import SQUARE_AMOUNT
from SnakeLogic import SnakeLogic


class RandomSearchPlus(SnakeLogic):
    def __init__(self):
        self.reset()
        self.defeated = False

    def move(self, food):
        potential_steps = self.generate_all_potential_steps()

        steps = []
        for u in potential_steps:
            flag = 1
            for d in self.body:
                if d == u:
                    flag = 0
            if flag:
                steps.append(u)

        if steps:
            self.body.insert(0, steps[random.randint(0,len(steps)-1)])
            self.checkAte(food, self.body)
        else:
            self.reset()
            self.defeated = True
        return self.body
