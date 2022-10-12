import pygame

from Directions import Directions
from DrawSnake import Snake

class Player(Snake):
    def play_step(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Directions.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Directions.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Directions.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Directions.DOWN

        self.move(self.direction)  # update the head
        self.snake.insert(0, self.head)

        if self.head == self.food:
            self.score += 1
        else:
            self.snake.pop()
