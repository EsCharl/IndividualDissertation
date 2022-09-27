import random

import pygame
from collections import namedtuple

pygame.init()

Point = namedtuple('Point', 'x y')

class Game:
    def __init__(self, width=640, height=480):
        width = width
        height = height

        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Snake Game')

        self.food = None

        self.bodyLength = 3


    def game_reset(self):
        self.bodyLength = 3

if __name__ == '__main__':
    Game()
