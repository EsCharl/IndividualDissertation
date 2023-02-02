import random

from SnakeLogic import SnakeLogic


class RandomSearchPlus(SnakeLogic):
    def __init__(self):
        super().__init__("Random Search")
        self.reset()
        self.defeated = False

    def move(self, food):
        potential_steps = self.generateAllPotentialSteps()

        steps = []
        for u in potential_steps:
            flag = 1
            for d in self.body:
                if d == u:
                    flag = 0
            if flag:
                steps.append(u)

        if steps:
            step = steps[random.randint(0,len(steps)-1)]
            self.body.insert(0, step)
            self.checkAte(food, self.body)
            return step
        else:
            self.reset()
            self.defeated = True
        return self.body
