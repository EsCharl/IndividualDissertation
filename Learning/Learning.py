import pygame

class LearningScreen:
    def __init__(self,w=640,h=480):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Learning Snake Game')

        color = (150,150,150)

        self.display.fill(color)
        while True:

            pygame.display.flip()