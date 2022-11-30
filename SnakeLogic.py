import random

import Constants


class SnakeLogic:
    def generate_all_potential_steps(self):
        steps = []
        if self.body[0][0] + 1 < Constants.SQUARE_AMOUNT:
            steps.append([self.body[0][0] + 1, self.body[0][1]])
        if self.body[0][0] - 1 >= 0:
            steps.append([self.body[0][0] - 1, self.body[0][1]])
        if self.body[0][1] + 1 < Constants.SQUARE_AMOUNT:
            steps.append([self.body[0][0], self.body[0][1] + 1])
        if self.body[0][1] - 1 >= 0:
            steps.append([self.body[0][0], self.body[0][1] - 1])
        return steps

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

    def checkAte(self, food, body):
        if not body[0] == [food.foodX, food.foodY]:
            self.body.pop()
