import pygame

from Directions import Directions

class Player:
    def __init__(self):
        self.direction = Directions.LEFT

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

        return self.direction