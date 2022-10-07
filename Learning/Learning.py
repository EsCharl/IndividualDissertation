import pygame

class LearningScreen:
    display = pygame.display.set_mode((960, 540))
    pygame.display.set_caption('Learning Snake Game')

    color = (150,150,150)

    display.fill(color)

if __name__ == '__main__':
    LearningScreen()
    while True:

        pygame.display.flip()