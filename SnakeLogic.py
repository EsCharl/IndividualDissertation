import random

import Constants


class SnakeLogic:
    def checkSnake(self):
        if self.body[0][0] < 0 or self.body[0][1] > Constants.SQUARE_AMOUNT - 1 or self.body[0][0] \
                > Constants.SQUARE_AMOUNT - 1 or self.body[0][1] < 0:
            self.reset()
        for x in self.body[1:]:
            if self.body[0] == x:
                self.reset()

    def reset(self):
        self.body = [[random.randint(2, Constants.SQUARE_AMOUNT - 3), random.randint(2, Constants.SQUARE_AMOUNT - 3)]]
        for x in range(0, 2):
            if random.randint(0, 1):
                self.body.append([self.body[x][0] + 1, self.body[x][1]])
            else:
                self.body.append([self.body[x][0], self.body[x][1] + 1])
        self.ate = False

    def checkAte(self):
        if self.ate:
            self.ate = False
        else:
            self.body.pop()
