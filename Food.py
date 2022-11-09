import random

from Constants import SQUARE_AMOUNT


class Food:
    def __init__(self, body):
        self.randomFood(body)

    def randomFood(self, body):
        self.foodX = random.randint(0, SQUARE_AMOUNT - 1)
        self.foodY = random.randint(0, SQUARE_AMOUNT - 1)
        for pixel in body:
            if pixel[0] == self.foodX and pixel[1] == self.foodY:
                self.randomFood(body)
