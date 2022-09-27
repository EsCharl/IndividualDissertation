from collections import namedtuple
from random import random

from Constants import BLOCK_PIXEL_SIZE
from Game import Game

Point = namedtuple('Point', 'x y')

def place_food(snakes):
    x = random.randint(0, (Game.width - BLOCK_PIXEL_SIZE) // BLOCK_PIXEL_SIZE) * BLOCK_PIXEL_SIZE
    y = random.randint(0, (Game.height - BLOCK_PIXEL_SIZE) // BLOCK_PIXEL_SIZE) * BLOCK_PIXEL_SIZE
    food = Point(x, y)
    if food in snakes:
        place_food()

    return food