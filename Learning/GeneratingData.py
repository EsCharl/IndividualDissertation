import os
import pickle
from datetime import datetime

import pygame as pg
import sys

sys.path.insert(0, os.path.abspath("../"))

import DrawSnake
import GameBoardSize
import PixelSize
from Algorithms.AlmightyMove import AlmightyMove
from Algorithms.AStar import AStar
from Algorithms.BestFirstSearchPlus import BestFirstSearchPlus
from Algorithms.RandomSearchPlus import RandomSearchPlus
from Constants import SQUARE_AMOUNT
from Food import Food
from Learning import EA

from UpdateValues import updateOtherFood, updateOtherAlgo, resetDefeat, clearSteps

gameBoardColour = (100, 50, 90)
SPEED = 5000


def updateSnake(canvas, snake, snake_food, square_size_side):
    DrawSnake.DrawSnake(canvas, snake.body, square_size_side)
    ate = False

    if (snake.body[0][0] == snake_food.foodX) and (snake.body[0][1] == snake_food.foodY):
        snake.checkSnake()
        ate = True

    return ate


def drawFood(canvas, ate, snake, snake_food, square_size_side):
    if ate:
        snake_food.randomFood(snake.body)

    # this is to draw the food
    pg.draw.rect(canvas, (255, 0, 0),
                 pg.Rect(snake_food.foodX * square_size_side, snake_food.foodY * square_size_side,
                         square_size_side, square_size_side))


def recordWinner(algo_name, folder):
    with open(folder + "/winners.txt", 'a') as f:
        f.write(algo_name + "\n")


def updateDirectory(dir1, dir2, dir3, dir4, dir5, num):
    D1 = os.path.join(dir1, str(num))
    D2 = os.path.join(dir2, str(num))
    D3 = os.path.join(dir3, str(num))
    D4 = os.path.join(dir4, str(num))
    D5 = os.path.join(dir5, str(num))

    os.mkdir(D1)
    os.mkdir(D2)
    os.mkdir(D3)
    os.mkdir(D4)
    os.mkdir(D5)

    return D1, D2, D3, D4, D5


def recordSteps(algo1, algo2, algo3, algo4, algo5, dir1, dir2, dir3, dir4, dir5, game_num, food):
    algo1.append([food.foodX, food.foodY])
    algo2.append([food.foodX, food.foodY])
    algo3.append([food.foodX, food.foodY])
    algo4.append([food.foodX, food.foodY])
    algo5.append([food.foodX, food.foodY])

    F1 = open(dir1 + "/" + str(game_num) + ".pickle", 'wb')
    pickle.dump(algo1, F1)
    F1.close()

    F2 = open(dir2 + "/" + str(game_num) + ".pickle", 'wb')
    pickle.dump(algo2, F2)
    F2.close()

    F3 = open(dir3 + "/" + str(game_num) + ".pickle", 'wb')
    pickle.dump(algo3, F3)
    F3.close()

    F4 = open(dir4 + "/" + str(game_num) + ".pickle", 'wb')
    pickle.dump(algo4, F4)
    F4.close()

    F5 = open(dir5 + "/" + str(game_num) + ".pickle", 'wb')
    pickle.dump(algo5, F5)
    F5.close()


def globalDraw(SA3, a_star, a_star_food, squareSizeSide, SA1, best_first_search_plus,
               best_first_search_plus_food, SA5, random_search_plus, random_search_plus_food, SA4, almighty_move,
               almighty_move_food, SA2, a_star_dynamic, a_star_dynamic_food):
    # to reset the canvas once a victor is selected
    SA1.fill(gameBoardColour)
    SA2.fill(gameBoardColour)
    SA3.fill(gameBoardColour)
    SA4.fill(gameBoardColour)
    SA5.fill(gameBoardColour)

    updateSnake(SA3, a_star, a_star_food, squareSizeSide)
    updateSnake(SA2, a_star_dynamic, a_star_dynamic_food, squareSizeSide)
    updateSnake(SA1, best_first_search_plus, best_first_search_plus_food, squareSizeSide)
    updateSnake(SA5, random_search_plus, random_search_plus_food, squareSizeSide)
    updateSnake(SA4, almighty_move, almighty_move_food, squareSizeSide)


class LearningScreen:

    def __init__(self, data=1000, pop_size=300, generation_limit=10, cross_over_prob=0.5, mutation_prob=0.2,
                 first_range_value=-15, second_range_value=15, w=640, h=400):

        if pop_size % 2:
            pop_size += 1

        now = datetime.now()

        FOLDER = "../data/" + now.strftime("%d_%m_%Y %H_%M_%S")

        os.mkdir(FOLDER)

        IMAGE_SAVE_FOLDER = FOLDER + "/Images/"
        STEPS_SAVE_FOLDER = FOLDER + "/Steps/"

        os.mkdir(IMAGE_SAVE_FOLDER)
        os.mkdir(STEPS_SAVE_FOLDER)

        pg.init()

        num_game = 0
        step = 0

        random_defeat = 0
        a_star_defeat = 0
        a_star_dynamic_defeat = 0
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
        SA2 = pg.Surface((boardSideSize, boardSideSize))
        SA3 = pg.Surface((boardSideSize, boardSideSize))
        SA4 = pg.Surface((boardSideSize, boardSideSize))
        SA5 = pg.Surface((boardSideSize, boardSideSize))

        # setup the player/AI objects (all takes the first part of the algorithm to have the same body and food position)
        a_star = AStar("A-Star Static")
        a_star_food = Food(a_star.body)

        a_star_dynamic = AStar("A-Star Dynamic")
        best_first_search_plus = BestFirstSearchPlus()
        random_search_plus = RandomSearchPlus()
        almighty_move = AlmightyMove()

        updateOtherAlgo(a_star, best_first_search_plus, random_search_plus, almighty_move, a_star_dynamic)

        best_first_search_plus_food = Food(best_first_search_plus.body)
        a_star_dynamic_food = Food(a_star_dynamic.body)
        random_search_plus_food = Food(random_search_plus.body)
        almighty_move_food = Food(almighty_move.body)

        updateOtherFood(a_star_food, almighty_move_food, best_first_search_plus_food, random_search_plus_food,
                        a_star_dynamic_food)

        a_star_body_moves = []
        a_star_body_dynamic_moves = []
        best_first_search_plus_body_moves = []
        random_search_plus_body_moves = []
        almighty_move_body_moves = []

        # this is to store the images
        a_star_file_dir_image = os.path.join(IMAGE_SAVE_FOLDER, a_star.name)
        a_star_dynamic_file_dir_image = os.path.join(IMAGE_SAVE_FOLDER, a_star_dynamic.name)
        best_first_search_plus_dir_image = os.path.join(IMAGE_SAVE_FOLDER, best_first_search_plus.name)
        random_search_plus_dir_image = os.path.join(IMAGE_SAVE_FOLDER, random_search_plus.name)
        almighty_move_dir_image = os.path.join(IMAGE_SAVE_FOLDER, almighty_move.name)

        os.mkdir(a_star_file_dir_image)
        os.mkdir(a_star_dynamic_file_dir_image)
        os.mkdir(best_first_search_plus_dir_image)
        os.mkdir(random_search_plus_dir_image)
        os.mkdir(almighty_move_dir_image)

        a_star_file_dirW, best_first_search_plus_dirW, random_search_plus_dirW, almighty_move_dirW, a_star_dynamic_file_dirW = updateDirectory(
            a_star_file_dir_image, best_first_search_plus_dir_image, random_search_plus_dir_image,
            almighty_move_dir_image, a_star_dynamic_file_dir_image, num_game)

        # this is to store the steps
        a_star_file_dir_steps = os.path.join(STEPS_SAVE_FOLDER, a_star.name)
        a_star_dynamic_file_dir_steps = os.path.join(STEPS_SAVE_FOLDER, a_star_dynamic.name)
        best_first_search_plus_dir_steps = os.path.join(STEPS_SAVE_FOLDER, best_first_search_plus.name)
        random_search_plus_dir_steps = os.path.join(STEPS_SAVE_FOLDER, random_search_plus.name)
        almighty_move_dir_steps = os.path.join(STEPS_SAVE_FOLDER, almighty_move.name)

        os.mkdir(a_star_file_dir_steps)
        os.mkdir(a_star_dynamic_file_dir_steps)
        os.mkdir(best_first_search_plus_dir_steps)
        os.mkdir(random_search_plus_dir_steps)
        os.mkdir(almighty_move_dir_steps)

        done = False

        init_body = []
        while not done and num_game < data:
            try:
                found_solution = False
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                        pg.quit()
                        quit()

                # this is used to get the initial body status (start of each round)
                if not init_body:
                    init_body = a_star.body.copy()

                SA1.fill(gameBoardColour)
                SA2.fill(gameBoardColour)
                SA3.fill(gameBoardColour)
                SA4.fill(gameBoardColour)
                SA5.fill(gameBoardColour)

                all_sprites.update()

                all_sprites.draw(screen)

                step += 1

                if not a_star_defeat and not found_solution:
                    if not a_star.path:
                        a_star.getPath(a_star_food)

                    if a_star.path:
                        body = a_star.body.copy()
                        a_star_body_moves.append([body, a_star.move(a_star_food)])

                    if updateSnake(SA3, a_star, a_star_food, squareSizeSide):
                        found_solution = True
                        updateOtherAlgo(a_star, best_first_search_plus, random_search_plus, almighty_move,
                                        a_star_dynamic)
                        recordSteps(a_star_body_dynamic_moves, best_first_search_plus_body_moves,
                                    almighty_move_body_moves, random_search_plus_body_moves,
                                    a_star_body_moves, a_star_dynamic_file_dir_steps, best_first_search_plus_dir_steps,
                                    almighty_move_dir_steps,
                                    random_search_plus_dir_steps, a_star_file_dir_steps, num_game, a_star_food)
                        a_star_body_dynamic_moves, best_first_search_plus_body_moves, almighty_move_body_moves, random_search_plus_body_moves, a_star_body_moves = clearSteps()

                        screen.blit(SA3, (50 + (boardSideSize * 2), 5))
                        pg.image.save(SA3, os.path.join(a_star_file_dirW, str(num_game) + "_" + str(step) + ".jpeg"))

                        drawFood(SA3, True, a_star, a_star_food, squareSizeSide)
                        updateOtherFood(a_star_food, best_first_search_plus_food, random_search_plus_food,
                                        almighty_move_food, a_star_dynamic_food)

                        print(a_star.name)
                        recordWinner(a_star.name, FOLDER)

                        almighty_defeat, best_first_defeat, random_defeat, a_star_defeat, a_star_dynamic_defeat = resetDefeat()
                        globalDraw(SA3, a_star, a_star_food, squareSizeSide, SA1, best_first_search_plus,
                                   best_first_search_plus_food, SA5, random_search_plus, random_search_plus_food,
                                   SA4, almighty_move, almighty_move_food, SA2, a_star_dynamic, a_star_dynamic_food)

                        num_game += 1
                        step = 0
                        a_star_file_dirW, best_first_search_plus_dirW, random_search_plus_dirW, almighty_move_dirW, a_star_dynamic_file_dirW = updateDirectory(
                            a_star_file_dir_image, best_first_search_plus_dir_image, random_search_plus_dir_image,
                            almighty_move_dir_image, a_star_dynamic_file_dir_image,
                            num_game)
                        a_star.path = []
                        a_star_dynamic.path = []
                        init_body = []

                if not best_first_defeat and not found_solution:
                    body = best_first_search_plus.body.copy()
                    move = best_first_search_plus.move(best_first_search_plus_food)
                    if move:
                        best_first_search_plus_body_moves.append([body, move])

                    if updateSnake(SA1, best_first_search_plus, best_first_search_plus_food, squareSizeSide):
                        found_solution = True
                        updateOtherAlgo(best_first_search_plus, a_star, random_search_plus, almighty_move,
                                        a_star_dynamic)
                        recordSteps(a_star_body_dynamic_moves, best_first_search_plus_body_moves,
                                    almighty_move_body_moves, random_search_plus_body_moves,
                                    a_star_body_moves, a_star_dynamic_file_dir_steps, best_first_search_plus_dir_steps,
                                    almighty_move_dir_steps,
                                    random_search_plus_dir_steps, a_star_file_dir_steps, num_game,
                                    best_first_search_plus_food)
                        a_star_body_dynamic_moves, best_first_search_plus_body_moves, almighty_move_body_moves, random_search_plus_body_moves, a_star_body_moves = clearSteps()

                        screen.blit(SA1, (10, 5))
                        pg.image.save(SA1, os.path.join(best_first_search_plus_dirW,
                                                        str(num_game) + "_" + str(step) + ".jpeg"))

                        drawFood(SA1, True, best_first_search_plus, best_first_search_plus_food, squareSizeSide)
                        updateOtherFood(best_first_search_plus_food, a_star_food, random_search_plus_food,
                                        almighty_move_food, a_star_dynamic_food)

                        print(best_first_search_plus.name)
                        recordWinner(best_first_search_plus.name, FOLDER)

                        almighty_defeat, best_first_defeat, random_defeat, a_star_defeat, a_star_dynamic_defeat = resetDefeat()
                        globalDraw(SA3, a_star, a_star_food, squareSizeSide, SA1, best_first_search_plus,
                                   best_first_search_plus_food, SA5, random_search_plus, random_search_plus_food,
                                   SA4, almighty_move, almighty_move_food, SA2, a_star_dynamic, a_star_dynamic_food)

                        num_game += 1
                        step = 0
                        a_star_file_dirW, best_first_search_plus_dirW, random_search_plus_dirW, almighty_move_dirW, a_star_dynamic_file_dirW = updateDirectory(
                            a_star_file_dir_image, best_first_search_plus_dir_image, random_search_plus_dir_image,
                            almighty_move_dir_image, a_star_dynamic_file_dir_image,
                            num_game)
                        a_star.path = []
                        a_star_dynamic.path = []
                        init_body = []

                if not random_defeat and not found_solution:
                    body = random_search_plus.body.copy()
                    move = random_search_plus.move(random_search_plus_food)
                    if move:
                        random_search_plus_body_moves.append([body, move])

                    if updateSnake(SA5, random_search_plus, random_search_plus_food, squareSizeSide):
                        found_solution = True
                        updateOtherAlgo(random_search_plus, best_first_search_plus, a_star, almighty_move,
                                        a_star_dynamic)
                        recordSteps(a_star_body_dynamic_moves, best_first_search_plus_body_moves,
                                    almighty_move_body_moves, random_search_plus_body_moves,
                                    a_star_body_moves, a_star_dynamic_file_dir_steps, best_first_search_plus_dir_steps,
                                    almighty_move_dir_steps,
                                    random_search_plus_dir_steps, a_star_file_dir_steps, num_game,
                                    random_search_plus_food)
                        a_star_body_dynamic_moves, best_first_search_plus_body_moves, almighty_move_body_moves, random_search_plus_body_moves, a_star_body_moves = clearSteps()

                        screen.blit(SA5, (50 + (boardSideSize * 2), boardSideSize + 10))
                        pg.image.save(SA5,
                                      os.path.join(random_search_plus_dirW, str(num_game) + "_" + str(step) + ".jpeg"))

                        drawFood(SA5, True, random_search_plus, random_search_plus_food, squareSizeSide)
                        updateOtherFood(random_search_plus_food, best_first_search_plus_food, a_star_food,
                                        almighty_move_food, a_star_dynamic_food)

                        print(random_search_plus.name)
                        recordWinner(random_search_plus.name, FOLDER)

                        almighty_defeat, best_first_defeat, random_defeat, a_star_defeat, a_star_dynamic_defeat = resetDefeat()
                        globalDraw(SA3, a_star, a_star_food, squareSizeSide, SA1, best_first_search_plus,
                                   best_first_search_plus_food, SA5, random_search_plus, random_search_plus_food,
                                   SA4, almighty_move, almighty_move_food, SA2, a_star_dynamic, a_star_dynamic_food)

                        num_game += 1
                        step = 0
                        a_star_file_dirW, best_first_search_plus_dirW, random_search_plus_dirW, almighty_move_dirW, a_star_dynamic_file_dirW = updateDirectory(
                            a_star_file_dir_image, best_first_search_plus_dir_image, random_search_plus_dir_image,
                            almighty_move_dir_image, a_star_dynamic_file_dir_image,
                            num_game)
                        a_star.path = []
                        a_star_dynamic.path = []
                        init_body = []

                if not almighty_defeat and not found_solution:
                    body = almighty_move.body.copy()
                    move = almighty_move.move(almighty_move_food)
                    if move:
                        almighty_move_body_moves.append([body, move])

                    if updateSnake(SA4, almighty_move, almighty_move_food, squareSizeSide):
                        found_solution = True
                        updateOtherAlgo(almighty_move, best_first_search_plus, random_search_plus, a_star,
                                        a_star_dynamic)
                        recordSteps(a_star_body_dynamic_moves, best_first_search_plus_body_moves,
                                    almighty_move_body_moves, random_search_plus_body_moves,
                                    a_star_body_moves, a_star_dynamic_file_dir_steps, best_first_search_plus_dir_steps,
                                    almighty_move_dir_steps,
                                    random_search_plus_dir_steps, a_star_file_dir_steps, num_game, almighty_move_food)
                        a_star_body_dynamic_moves, best_first_search_plus_body_moves, almighty_move_body_moves, random_search_plus_body_moves, a_star_body_moves = clearSteps()

                        screen.blit(SA4, (10, boardSideSize + 10))
                        pg.image.save(SA4, os.path.join(almighty_move_dirW, str(num_game) + "_" + str(step) + ".jpeg"))

                        drawFood(SA4, True, almighty_move, almighty_move_food, squareSizeSide)
                        updateOtherFood(almighty_move_food, best_first_search_plus_food, random_search_plus_food,
                                        a_star_food, a_star_dynamic_food)

                        print(almighty_move.name)
                        recordWinner(almighty_move.name, FOLDER)

                        almighty_defeat, best_first_defeat, random_defeat, a_star_defeat, a_star_dynamic_defeat = resetDefeat()
                        globalDraw(SA3, a_star, a_star_food, squareSizeSide, SA1, best_first_search_plus,
                                   best_first_search_plus_food, SA5, random_search_plus, random_search_plus_food,
                                   SA4, almighty_move, almighty_move_food, SA2, a_star_dynamic, a_star_dynamic_food)

                        num_game += 1
                        step = 0
                        a_star_file_dirW, best_first_search_plus_dirW, random_search_plus_dirW, almighty_move_dirW, a_star_dynamic_file_dirW = updateDirectory(
                            a_star_file_dir_image, best_first_search_plus_dir_image, random_search_plus_dir_image,
                            almighty_move_dir_image, a_star_dynamic_file_dir_image,
                            num_game)
                        a_star.path = []
                        a_star_dynamic.path = []
                        init_body = []

                if not a_star_dynamic_defeat and not found_solution:
                    a_star_dynamic.getPath(a_star_food)

                    if a_star_dynamic.path:
                        body = a_star_dynamic.body.copy()
                        a_star_body_dynamic_moves.append([body, a_star_dynamic.move(a_star_food)])

                    if updateSnake(SA2, a_star_dynamic, a_star_dynamic_food, squareSizeSide):
                        found_solution = True
                        updateOtherAlgo(a_star_dynamic, a_star, best_first_search_plus, random_search_plus,
                                        almighty_move)
                        recordSteps(a_star_body_dynamic_moves, best_first_search_plus_body_moves,
                                    almighty_move_body_moves, random_search_plus_body_moves,
                                    a_star_body_moves, a_star_dynamic_file_dir_steps, best_first_search_plus_dir_steps,
                                    almighty_move_dir_steps,
                                    random_search_plus_dir_steps, a_star_file_dir_steps, num_game, a_star_dynamic_food)
                        a_star_body_dynamic_moves, best_first_search_plus_body_moves, almighty_move_body_moves, random_search_plus_body_moves, a_star_body_moves = clearSteps()

                        screen.blit(SA2, (boardSideSize + 30, 5))
                        pg.image.save(SA2,
                                      os.path.join(a_star_dynamic_file_dirW, str(num_game) + "_" + str(step) + ".jpeg"))

                        drawFood(SA2, True, a_star_dynamic, a_star_dynamic_food, squareSizeSide)
                        updateOtherFood(a_star_dynamic_food, best_first_search_plus_food, random_search_plus_food,
                                        almighty_move_food, a_star_food)

                        print(a_star_dynamic.name)
                        recordWinner(a_star_dynamic.name, FOLDER)

                        almighty_defeat, best_first_defeat, random_defeat, a_star_defeat, a_star_dynamic_defeat = resetDefeat()
                        globalDraw(SA3, a_star, a_star_food, squareSizeSide, SA1, best_first_search_plus,
                                   best_first_search_plus_food, SA5, random_search_plus, random_search_plus_food,
                                   SA4, almighty_move, almighty_move_food, SA2, a_star_dynamic, a_star_dynamic_food)

                        num_game += 1
                        step = 0
                        a_star_file_dirW, best_first_search_plus_dirW, random_search_plus_dirW, almighty_move_dirW, a_star_dynamic_file_dirW = updateDirectory(
                            a_star_file_dir_image, best_first_search_plus_dir_image, random_search_plus_dir_image,
                            almighty_move_dir_image, a_star_dynamic_file_dir_image,
                            num_game)
                        a_star.path = []
                        a_star_dynamic.path = []
                        init_body = []

                if almighty_defeat and random_defeat and a_star_defeat and best_first_defeat:
                    updateOtherAlgo(a_star, best_first_search_plus, random_search_plus, almighty_move, a_star_dynamic)

                    # this section is to ensure if no step was recorded it will have at least the body to support it.
                    if not a_star_body_dynamic_moves:
                        a_star_body_dynamic_moves = [[init_body, []]]
                    if not best_first_search_plus_body_moves:
                        best_first_search_plus_body_moves = [[init_body, []]]
                    if not almighty_move_body_moves:
                        almighty_move_body_moves = [[init_body, []]]
                    if not random_search_plus_body_moves:
                        random_search_plus_body_moves = [[init_body, []]]
                    if not a_star_body_moves:
                        a_star_body_moves = [[init_body, []]]

                    recordSteps(a_star_body_dynamic_moves, best_first_search_plus_body_moves,
                                almighty_move_body_moves, random_search_plus_body_moves,
                                a_star_body_moves, a_star_dynamic_file_dir_steps, best_first_search_plus_dir_steps,
                                almighty_move_dir_steps,
                                random_search_plus_dir_steps, a_star_file_dir_steps, num_game, a_star_food)
                    drawFood(SA3, True, a_star, a_star_food, squareSizeSide)
                    updateOtherFood(a_star_food, best_first_search_plus_food, random_search_plus_food,
                                    almighty_move_food, a_star_dynamic_food)
                    a_star_body_dynamic_moves, best_first_search_plus_body_moves, almighty_move_body_moves, random_search_plus_body_moves, a_star_body_moves = clearSteps()

                    print("no victor")
                    recordWinner("None", FOLDER)

                    almighty_defeat, best_first_defeat, random_defeat, a_star_defeat, a_star_dynamic_defeat = resetDefeat()
                    globalDraw(SA3, a_star, a_star_food, squareSizeSide, SA1, best_first_search_plus,
                               best_first_search_plus_food, SA5, random_search_plus, random_search_plus_food,
                               SA4, almighty_move, almighty_move_food, SA2, a_star_dynamic, a_star_dynamic_food)

                    num_game += 1
                    step = 0
                    a_star_file_dirW, best_first_search_plus_dirW, random_search_plus_dirW, almighty_move_dirW, a_star_dynamic_file_dirW = updateDirectory(
                        a_star_file_dir_image, best_first_search_plus_dir_image, random_search_plus_dir_image,
                        almighty_move_dir_image, a_star_dynamic_file_dir_image,
                        num_game)
                    a_star.path = []
                    a_star_dynamic.path = []
                    init_body = []

                random_defeat = random_search_plus.defeated
                almighty_defeat = almighty_move.defeated
                a_star_defeat = a_star.defeated
                a_star_dynamic_defeat = a_star_dynamic.defeated
                best_first_defeat = best_first_search_plus.defeated

                if not best_first_defeat:
                    drawFood(SA1, False, best_first_search_plus, best_first_search_plus_food, squareSizeSide)
                    screen.blit(SA1, (10, 5))
                    pg.image.save(SA1,
                                  os.path.join(best_first_search_plus_dirW, str(num_game) + "_" + str(step) + ".jpeg"))

                if not a_star_defeat:
                    drawFood(SA3, False, a_star, a_star_food, squareSizeSide)
                    screen.blit(SA3, (50 + (boardSideSize * 2), 5))
                    pg.image.save(SA3, os.path.join(a_star_file_dirW, str(num_game) + "_" + str(step) + ".jpeg"))

                if not a_star_dynamic_defeat:
                    drawFood(SA2, False, a_star_dynamic, a_star_dynamic_food, squareSizeSide)
                    screen.blit(SA2, (boardSideSize + 30, 5))
                    pg.image.save(SA2,
                                  os.path.join(a_star_dynamic_file_dirW, str(num_game) + "_" + str(step) + ".jpeg"))

                if not almighty_defeat:
                    drawFood(SA4, False, almighty_move, almighty_move_food, squareSizeSide)
                    screen.blit(SA4, (10, boardSideSize + 10))
                    pg.image.save(SA4, os.path.join(almighty_move_dirW, str(num_game) + "_" + str(step) + ".jpeg"))

                if not random_defeat:
                    drawFood(SA5, False, random_search_plus, random_search_plus_food, squareSizeSide)
                    screen.blit(SA5, (50 + (boardSideSize * 2), boardSideSize + 10))
                    pg.image.save(SA5, os.path.join(random_search_plus_dirW, str(num_game) + "_" + str(step) + ".jpeg"))

                pg.display.update()

                clock.tick(SPEED)

            except KeyboardInterrupt:
                quit()

        pg.quit()
        EA.main(FOLDER, pop_size, generation_limit, cross_over_prob, mutation_prob, first_range_value, second_range_value)


if __name__ == '__main__':
    LearningScreen()
