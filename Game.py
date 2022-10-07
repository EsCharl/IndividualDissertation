import pygame

pygame.init()

class GameScreen:
    display = pygame.display.set_mode((960, 540))
    pygame.display.set_caption('Snake Game')

    color = (150,150,150)

    display.fill(color)

if __name__ == '__main__':
    GameScreen()
    while True:

        pygame.display.flip()
