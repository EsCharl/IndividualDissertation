import os
from datetime import datetime

import pygame as pg

import tensorflow
import DrawSnake
import GameBoardSize
import PixelSize
from Algorithms.AlmightyMove import AlmightyMove
from Algorithms.AStar_old import AStar
from Algorithms.BestFirstSearchPlus import BestFirstSearchPlus
from Algorithms.RandomSearchPlus import RandomSearchPlus
from Constants import SQUARE_AMOUNT
from Food import Food
import copy

from Learning.Evaluation import accumulationEvaluation
from Learning.UpdateValues import updateOtherFood, updateOtherAlgo, resetDefeat, clearSteps

gameBoardColour = (100, 50, 90)
SPEED = 20
now = datetime.now()

IMAGE_SAVE_FOLDER = "../Images/"+now.strftime("%d_%m_%Y %H_%M_%S")
STEPS_SAVE_FOLDER = "../Steps/"+now.strftime("%d_%m_%Y %H_%M_%S")

os.mkdir(IMAGE_SAVE_FOLDER)
os.mkdir(STEPS_SAVE_FOLDER)
def drawing(canvas, snake, snake_food, square_size_side):
    DrawSnake.DrawSnake(canvas, snake.body, square_size_side)
    ate = False

    if (snake.body[0][0] == snake_food.foodX) and (snake.body[0][1] == snake_food.foodY):
        snake.checkSnake()
        snake_food.randomFood(snake.body)
        ate = True

    pg.draw.rect(canvas, (255, 0, 0),
                 pg.Rect(snake_food.foodX * square_size_side, snake_food.foodY * square_size_side,
                         square_size_side, square_size_side))

    if ate:
        return True
    else:
        return False

class LearningScreen:

    def updateDirectory(self, dir1, dir2, dir3, dir4, num):
        D1 = os.path.join(dir1, str(num))
        D2 = os.path.join(dir2, str(num))
        D3 = os.path.join(dir3, str(num))
        D4 = os.path.join(dir4, str(num))

        os.mkdir(D1)
        os.mkdir(D2)
        os.mkdir(D3)
        os.mkdir(D4)

        return D1, D2, D3, D4

    def globalDraw(self, SA3, a_star, a_star_food, squareSizeSide, SA1, best_first_search_plus, best_first_search_plus_food, SA5, random_search_plus, random_search_plus_food, SA4, almighty_move, almighty_move_food):
        drawing(SA3, a_star, a_star_food, squareSizeSide)
        drawing(SA1, best_first_search_plus, best_first_search_plus_food, squareSizeSide)
        drawing(SA5, random_search_plus, random_search_plus_food, squareSizeSide)
        drawing(SA4, almighty_move, almighty_move_food, squareSizeSide)

    def __init__(self, w=640, h=480):
        pg.init()

        num_game = 0
        step = 0

        random_defeat = 0
        a_star_defeat = 0
        almighty_defeat = 0
        best_first_defeat = 0

        self.w = w
        self.h = h
        screen = pg.display.set_mode((self.w, self.h))
        screen.fill((20, 40, 70))
        pg.display.update()
        clock = pg.time.Clock()
        all_sprites = pg.sprite.Group()

        boardSideSize = GameBoardSize.get_size(self.w)
        squareSizeSide = PixelSize.get_block_size(boardSideSize, SQUARE_AMOUNT)

        SA1 = pg.Surface((boardSideSize, boardSideSize))
        SA3 = pg.Surface((boardSideSize, boardSideSize))
        SA4 = pg.Surface((boardSideSize, boardSideSize))
        SA5 = pg.Surface((boardSideSize, boardSideSize))

        # setup the player/AI objects (all takes the first part of the algorithm to have the same body and food position)
        a_star = AStar()
        a_star_food = Food(a_star.body)

        best_first_search_plus = BestFirstSearchPlus()
        random_search_plus = RandomSearchPlus()
        almighty_move = AlmightyMove()

        updateOtherAlgo(a_star, best_first_search_plus, random_search_plus, almighty_move)

        best_first_search_plus_food = Food(best_first_search_plus.body)
        random_search_plus_food = Food(random_search_plus.body)
        almighty_move_food = Food(almighty_move.body)

        updateOtherFood(a_star_food, almighty_move_food, best_first_search_plus_food, random_search_plus_food)

        a_star_moves = []
        best_first_search_plus_moves = []
        random_search_plus_moves = []
        almighty_move_moves = []

        # this is to store the images
        a_star_file_dir = os.path.join(IMAGE_SAVE_FOLDER, a_star.name)
        best_first_search_plus_dir = os.path.join(IMAGE_SAVE_FOLDER, best_first_search_plus.name)
        random_search_plus_dir = os.path.join(IMAGE_SAVE_FOLDER, random_search_plus.name)
        almighty_move_dir = os.path.join(IMAGE_SAVE_FOLDER, almighty_move.name)

        os.mkdir(a_star_file_dir)
        os.mkdir(best_first_search_plus_dir)
        os.mkdir(random_search_plus_dir)
        os.mkdir(almighty_move_dir)

        a_star_file_dirW, best_first_search_plus_dirW, random_search_plus_dirW, almighty_move_dirW = self.updateDirectory(a_star_file_dir, best_first_search_plus_dir, random_search_plus_dir, almighty_move_dir, num_game)

        done = False
        while not done:
            try:
                found_solution = False
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                        pg.quit()
                        quit()

                SA1.fill(gameBoardColour)
                SA3.fill(gameBoardColour)
                SA4.fill(gameBoardColour)
                SA5.fill(gameBoardColour)

                all_sprites.update()

                all_sprites.draw(screen)

                step += 1

                if not a_star.defeated and not found_solution:
                    if not a_star.path:
                        a_star.getPath(a_star_food)

                    if a_star.path:
                        a_star_moves.append(a_star.move(a_star_food))

                    if drawing(SA3, a_star, a_star_food, squareSizeSide):
                        found_solution = True
                        updateOtherAlgo(a_star, best_first_search_plus, random_search_plus, almighty_move)
                        updateOtherFood(a_star_food, best_first_search_plus_food, random_search_plus_food,
                                               almighty_move_food)
                        best_first_search_plus_moves, almighty_move_moves, random_search_plus_moves, a_star_moves = clearSteps()
                        print(a_star.name, accumulationEvaluation(a_star, a_star_food))
                        almighty_defeat, best_first_defeat, random_defeat, a_star_defeat = resetDefeat()
                        self.globalDraw(SA3, a_star, a_star_food, squareSizeSide, SA1, best_first_search_plus,
                                       best_first_search_plus_food, SA5, random_search_plus, random_search_plus_food, SA4,
                                       almighty_move, almighty_move_food)
                        # print(len(a_star.body), len(best_first_search_plus.body), len(almighty_move.body),
                        #       len(random_search_plus.body))
                        num_game += 1
                        step = 0
                        a_star_file_dirW, best_first_search_plus_dirW, random_search_plus_dirW, almighty_move_dirW = self.updateDirectory(
                            a_star_file_dir, best_first_search_plus_dir, random_search_plus_dir, almighty_move_dir,
                            num_game)
                        a_star.path = []

                if not best_first_search_plus.defeated and not found_solution:
                    best_first_search_plus_moves.append(best_first_search_plus.move(best_first_search_plus_food))
                    if drawing(SA1, best_first_search_plus, best_first_search_plus_food, squareSizeSide):
                        found_solution = True
                        updateOtherAlgo(best_first_search_plus, a_star, random_search_plus, almighty_move)
                        updateOtherFood(best_first_search_plus_food, a_star_food, random_search_plus_food,
                                               almighty_move_food)
                        best_first_search_plus_moves, almighty_move_moves, random_search_plus_moves, a_star_moves = clearSteps()
                        # print(len(a_star.body), len(best_first_search_plus.body), len(almighty_move.body),
                        #       len(random_search_plus.body))
                        print(best_first_search_plus.name, accumulationEvaluation(best_first_search_plus, best_first_search_plus_food))
                        almighty_defeat, best_first_defeat, random_defeat, a_star_defeat = resetDefeat()
                        self.globalDraw(SA3, a_star, a_star_food, squareSizeSide, SA1, best_first_search_plus,
                                       best_first_search_plus_food, SA5, random_search_plus, random_search_plus_food, SA4,
                                       almighty_move, almighty_move_food)
                        num_game += 1
                        step = 0
                        a_star_file_dirW, best_first_search_plus_dirW, random_search_plus_dirW, almighty_move_dirW = self.updateDirectory(
                            a_star_file_dir, best_first_search_plus_dir, random_search_plus_dir, almighty_move_dir,
                            num_game)
                        a_star.path = []

                if not random_search_plus.defeated and not found_solution:
                    random_search_plus_moves.append(random_search_plus.move(random_search_plus_food))

                    print(step, random_search_plus_moves)

                    if drawing(SA5, random_search_plus, random_search_plus_food, squareSizeSide):
                        # print("random search")
                        found_solution = True
                        updateOtherAlgo(random_search_plus, best_first_search_plus, a_star, almighty_move)
                        updateOtherFood(random_search_plus_food, best_first_search_plus_food, a_star_food,
                                               almighty_move_food)
                        best_first_search_plus_moves, almighty_move_moves, random_search_plus_moves, a_star_moves = clearSteps()
                        # print(len(a_star.body), len(best_first_search_plus.body), len(almighty_move.body),
                        #       len(random_search_plus.body))
                        print(random_search_plus.name,
                              accumulationEvaluation(random_search_plus, random_search_plus_food))
                        almighty_defeat, best_first_defeat, random_defeat, a_star_defeat = resetDefeat()
                        self.globalDraw(SA3, a_star, a_star_food, squareSizeSide, SA1, best_first_search_plus,
                                       best_first_search_plus_food, SA5, random_search_plus, random_search_plus_food, SA4,
                                       almighty_move, almighty_move_food)
                        num_game += 1
                        step = 0
                        a_star_file_dirW, best_first_search_plus_dirW, random_search_plus_dirW, almighty_move_dirW = self.updateDirectory(
                            a_star_file_dir, best_first_search_plus_dir, random_search_plus_dir, almighty_move_dir,
                            num_game)
                        a_star.path = []

                if not almighty_move.defeated and not found_solution:
                    almighty_move_moves.append(almighty_move.move(almighty_move_food))
                    if drawing(SA4, almighty_move, almighty_move_food, squareSizeSide):
                        updateOtherAlgo(almighty_move, best_first_search_plus, random_search_plus, a_star)
                        updateOtherFood(almighty_move_food, best_first_search_plus_food, random_search_plus_food,
                                               a_star_food)
                        best_first_search_plus_moves, almighty_move_moves, random_search_plus_moves, a_star_moves = clearSteps()
                        # print(len(a_star.body), len(best_first_search_plus.body), len(almighty_move.body),
                        #       len(random_search_plus.body))
                        almighty_defeat, best_first_defeat, random_defeat, a_star_defeat = resetDefeat()
                        print(almighty_move.name, accumulationEvaluation(random_search_plus, random_search_plus_food))
                        self.globalDraw(SA3, a_star, a_star_food, squareSizeSide, SA1, best_first_search_plus,
                                       best_first_search_plus_food, SA5, random_search_plus, random_search_plus_food, SA4,
                                       almighty_move, almighty_move_food)
                        num_game += 1
                        step = 0
                        a_star_file_dirW, best_first_search_plus_dirW, random_search_plus_dirW, almighty_move_dirW = self.updateDirectory(
                            a_star_file_dir, best_first_search_plus_dir, random_search_plus_dir, almighty_move_dir,
                            num_game)
                        a_star.path = []

                if almighty_move.defeated and random_search_plus.defeated and a_star.defeated and best_first_search_plus.defeated:
                    updateOtherAlgo(a_star, best_first_search_plus, random_search_plus, almighty_move)
                    updateOtherFood(a_star_food, best_first_search_plus_food, random_search_plus_food,
                                           almighty_move_food)
                    best_first_search_plus_moves, almighty_move_moves, random_search_plus_moves, a_star_moves = clearSteps()
                    # print(len(a_star.body), len(best_first_search_plus.body), len(almighty_move.body),
                    #       len(random_search_plus.body))
                    almighty_defeat, best_first_defeat, random_defeat, a_star_defeat = resetDefeat()
                    print("no victor")

                    self.globalDraw(SA3, a_star, a_star_food, squareSizeSide, SA1, best_first_search_plus,
                                   best_first_search_plus_food, SA5, random_search_plus, random_search_plus_food, SA4,
                                   almighty_move, almighty_move_food)
                    step = 0
                    num_game += 1
                    a_star_file_dirW, best_first_search_plus_dirW, random_search_plus_dirW, almighty_move_dirW = self.updateDirectory(
                        a_star_file_dir, best_first_search_plus_dir, random_search_plus_dir, almighty_move_dir,
                        num_game)

                if not best_first_defeat:
                    screen.blit(SA1, (10, 5))
                    pg.image.save(SA1, os.path.join(best_first_search_plus_dirW, str(num_game) + "_" + str(step)+".jpeg"))


                if not a_star_defeat:
                    screen.blit(SA3, (50 + (boardSideSize * 2), 5))
                    pg.image.save(SA3, os.path.join(a_star_file_dirW, str(num_game) + "_" + str(step)+".jpeg"))


                if not almighty_defeat:
                    screen.blit(SA4, (10, boardSideSize + 10))
                    pg.image.save(SA4, os.path.join(almighty_move_dirW, str(num_game) + "_" + str(step)+".jpeg"))


                if not random_defeat:
                    screen.blit(SA5, (50 + (boardSideSize * 2), boardSideSize + 10))
                    pg.image.save(SA5, os.path.join(random_search_plus_dirW, str(num_game) + "_" + str(step)+".jpeg"))

                random_defeat = random_search_plus.defeated
                almighty_defeat = almighty_move.defeated
                a_star_defeat = a_star.defeated
                best_first_defeat = best_first_search_plus.defeated

                pg.display.update()


                clock.tick(SPEED)

            except KeyboardInterrupt:
                quit()
