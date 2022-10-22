import random

import pygame

from Directions import Directions
from SnakeLogic import SnakeLogic


class Player(SnakeLogic):
    def __init__(self):
        self.direction = Directions.RIGHT
        self.reset()

    def reset(self):
        super().reset()
        self.direction = Directions.RIGHT

    def play_step(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.direction = Directions.LEFT
            elif event.key == pygame.K_RIGHT:
                self.direction = Directions.RIGHT
            elif event.key == pygame.K_UP:
                self.direction = Directions.UP
            elif event.key == pygame.K_DOWN:
                self.direction = Directions.DOWN

    def move(self):
        if self.direction == Directions.LEFT:
            self.body.insert(0, [self.body[0][0] - 1, self.body[0][1]])
        elif self.direction == Directions.RIGHT:
            self.body.insert(0, [self.body[0][0] + 1, self.body[0][1]])
        elif self.direction == Directions.UP:
            self.body.insert(0, [self.body[0][0], self.body[0][1] - 1])
        else:
            self.body.insert(0, [self.body[0][0], self.body[0][1] + 1])
