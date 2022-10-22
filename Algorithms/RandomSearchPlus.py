import random

from Constants import squareAmount
from SnakeLogic import SnakeLogic


class RandomSearchPlus(SnakeLogic):
    def __init__(self):
        self.reset()

    def move(self):
        print(self.body)
        potential_steps = []

        if self.body[0][0] + 1 < squareAmount:
            potential_steps.append([self.body[0][0] + 1, self.body[0][1]])
        if self.body[0][0] - 1 >= 0:
            potential_steps.append([self.body[0][0] - 1, self.body[0][1]])
        if self.body[0][1] + 1 < squareAmount:
            potential_steps.append([self.body[0][0], self.body[0][1] + 1])
        if self.body[0][1] - 1 >= 0:
            potential_steps.append([self.body[0][0], self.body[0][1] -1])

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
            self.checkAte()
        else:
            self.reset()
        return self.body
