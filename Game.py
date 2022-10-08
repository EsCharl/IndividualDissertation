import pygame

pygame.init()

class GameScreen:
    def __init__(self, w=640, h=480, time = 3):
        self.w = w
        self.h = h
        self.time = time

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake Game')

        color = (150, 150, 150)

        self.display.fill(color)
        while True:

            pygame.display.flip()
