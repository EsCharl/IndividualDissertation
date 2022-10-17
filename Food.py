import random

class Food:
    def __init__(self, body):
        self.randomFood(body)

    def randomFood(self, body):
        self.foodX = random.randint(0, 14)
        self.foodY = random.randint(0, 14)
        for pixel in body:
            if pixel[0] == self.foodX and pixel[1] == self.foodY:
                self.randomFood(body)
