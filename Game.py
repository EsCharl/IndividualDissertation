import random
import pygame
from collections import namedtuple

pygame.init()

Point = namedtuple('Point', 'x y')

class Game:
    display = pygame.display.set_mode((960, 540))
    pygame.display.set_caption('Snake Game')

    color = (150,150,150)

    display.fill(color)

if __name__ == '__main__':
    Game()
    while True:

        pygame.display.flip()
