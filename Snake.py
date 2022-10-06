from random import random
from collections import namedtuple

import numpy as np

import Food
from Constants import BLOCK_PIXEL_SIZE
from Directions import Directions
from Game import Game

Point = namedtuple('Point', 'x y')
class Snake(object):
    def game_reset(self):
        self.bodyLength = 3

    def reset(self):
        bodyGenerationTries = 0
        self.direction = Directions.Right
        self.head = Point(random(0, self.width), random(0, self.height))
        self.snake.append(self.head)

        for i in Game.bodyLength-1:

            body = self.picking_body_location()
            if (body == self.snake):
                if bodyGenerationTries == 100:
                    Game.game_reset()
                body = self.picking_body_location()
                bodyGenerationTries += 1

        self.snake.append(body)

    def picking_body_location(self):
        if (random.getrandbits(1)):
            body = Point(self.head.x + 1 if random.random() < 0.5 else -1, self.head.y)
        else:
            body = Point(self.head.x, self.head.y + 1 if random.random() < 0.5 else -1)
        return body

    def play_step(self, action):
        self.frame_iteration += 1

        self.move(action)
        self.snake.insert(0, self.head)

        reward = 0
        gameOver = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            gameOver = True

        if self.head == Food.food:
            winner = self.name
            Game.bodyLength += 1
        else:
            self.snake.pop()

    def move(self, action):
        clock_wise = [Directions.RIGHT, Directions.DOWN, Directions.LEFT, Directions.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Directions.RIGHT:
            x += BLOCK_PIXEL_SIZE
        elif self.direction == Directions.LEFT:
            x -= BLOCK_PIXEL_SIZE
        elif self.direction == Directions.DOWN:
            y += BLOCK_PIXEL_SIZE
        elif self.direction == Directions.UP:
            y -= BLOCK_PIXEL_SIZE

        self.head = Point(x, y)