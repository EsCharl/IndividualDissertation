import os
import sys

sys.path.insert(0, os.path.abspath("../"))

from datetime import datetime
import pygame as pg

import DrawSnake
import EvalConstants

from threading import Timer

from EvalBoardSize import get_size
import PixelSize
from Algorithms.Model import Model
from Evaluation.AccumulationAlgo import AccumulationAlgo
from Food import Food

gameBoardColour = (20, 50, 90)
backgroundColour = (20, 40, 70)

def drawGame(canvas, snake, snake_food, square_size_side):
    score = 0
    # draw the snake on the board
    DrawSnake.DrawSnake(canvas, snake.body, square_size_side)

    if (snake.body[0][0] == snake_food.foodX) and (snake.body[0][1] == snake_food.foodY):
        score = 1
        snake.checkSnake()
        snake_food.randomFood(snake.body)

    # draws the food
    pg.draw.rect(canvas, (255, 0, 0),
                 pg.Rect(snake_food.foodX * square_size_side, snake_food.foodY * square_size_side,
                         square_size_side, square_size_side))

    # for score
    return score

class Evaluation():
    def __init__(self, time, w=640, h=400):
        self.w = w
        self.h = h

        self.time = time
        self.num_reset = 0
        self.num_food_gained = 0

        # starting is the first round
        self.num_rounds = 1

        self.done = False

    def start(self, name, test_num):
        boardSideSize = get_size(self.h)
        squareSizeSide = PixelSize.get_block_size(boardSideSize, EvalConstants.SQUARE_AMOUNT)

        UI_position = [self.w - ((self.w - self.h) / 2), self.h / 2]

        boardSideSize = get_size(self.h)

        # this part is used to end the game after a certain amount of time.
        def gameEnd():
            self.done = True
            return

        for i in range(test_num):
            pg.init()

            font_renderer = pg.font.SysFont('Arial', int(25 * self.h / 768), bold=True)

            screen = pg.display.set_mode((self.w, self.h))
            pg.display.update()
            clock = pg.time.Clock()
            all_sprites = pg.sprite.Group()

            if name == "model":
                file = open("../Learning/result.txt", "r")

                text = file.read().split("\n")

                temp = text[-3].split("is ")[1]
                temp = temp.split(" at")[0]
                values = temp.split(",")
                final_values = []
                for i in values:
                    final_values.append(float(i))

                agent = Model(final_values)
            else:
                agent = AccumulationAlgo(name)

            agent_food = Food(agent.body)

            SM = pg.Surface((boardSideSize, boardSideSize))

            game_start = datetime.now()
            self.num_reset = 0
            self.num_food_gained = 0

            # starting is the first round
            self.num_rounds = 1
            self.done = False

            t = Timer(self.time * 60, gameEnd)
            t.start()

            while not self.done:
                try:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            self.done = True
                            pg.quit()
                            t.cancel()
                            quit()

                    screen.fill(backgroundColour)
                    SM.fill(gameBoardColour)

                    all_sprites.update()
                    all_sprites.draw(screen)

                    agent.move(agent_food)
                    all_sprites.draw(screen)

                    if agent.defeated:
                        agent.defeated = False
                        self.num_reset += 1
                        self.num_rounds += 1

                    if drawGame(SM, agent, agent_food, squareSizeSide):
                        self.num_food_gained += 1
                        self.num_rounds += 1

                    label = font_renderer.render(
                        str(self.num_rounds)+", "+str(self.num_reset)+", "+str(self.num_food_gained),  # The font to render
                        True,  # With anti aliasing
                        (255, 0, 0))

                    time = font_renderer.render(
                        str(int(self.time * 60 - (datetime.now() - game_start).total_seconds())), True, (255, 0, 0))

                    screen.blit(SM, (10, 5))
                    screen.blit(label, (UI_position[0], UI_position[1]))
                    screen.blit(time, (UI_position[0], 5))

                    pg.display.update()

                    clock.tick(EvalConstants.SPEED)

                except KeyboardInterrupt:
                    t.cancel()
            else:
                game_score_saving = "Score"

                if not os.path.exists(game_score_saving):
                    os.makedirs(game_score_saving)

                with open(game_score_saving + "/" + name + ".txt", 'a') as f:
                    f.write(str(self.num_rounds)+", "+str(self.num_reset)+", "+str(self.num_food_gained) + "\n")

                pg.quit()
        sys.exit()


if __name__ == '__main__':
    eval_project = Evaluation(3)

    eval_project.start("algo", 10)
