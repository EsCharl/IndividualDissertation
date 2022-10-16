import random

class Food:
    def __init__(self):
        self.randomFood()

    def randomFood(self):
        self.foodX = random.randint(0, 14)
        self.foodY = random.randint(0, 14)
