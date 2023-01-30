import pygame as pg

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

gameBoardColour = (100, 50, 90)
SPEED = 50

# this is the weight for the training (might have different implementation down the line)
training_weight = [0,0,0,0,0,0]

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
    def update_other_algo(self, main_algo, algo1, algo2, algo3):
        algo1.body = copy.copy(main_algo.body)
        algo2.body = copy.copy(main_algo.body)
        algo3.body = copy.copy(main_algo.body)

        algo1.defeated = False
        algo2.defeated = False
        algo3.defeated = False
        main_algo.defeated = False

    def update_other_food(self, main_food, algo1food, algo2food, algo3food):
        algo1food.foodX = main_food.foodX
        algo1food.foodY = main_food.foodY

        algo2food.foodX = main_food.foodX
        algo2food.foodY = main_food.foodY

        algo3food.foodX = main_food.foodX
        algo3food.foodY = main_food.foodY

    # this function is used for evaluation of the move.
    # If the move made can reach the food then it will be considered (score > 0 else score = 0).
    # from "Snake game AI: Movement rating functions and evolutionary algorithm-based optimization"
    def foodMoveEvaluation(self,space_value, space_list, food, possible_head):
        # the distance is the distance if the snake makes the move to there
        if food in space_list:
            distance = abs(possible_head[0] - food[0])+abs(possible_head[1] - food[1])
            score = space_value / distance
        else:
            score = 0
        return score

    # this will generate and select the best evaluation based on the available move (Left, Forward, Right)
    def accumulationEvaluation(self, snake, food):

        final_scores = []

        # the move_list is a list with 3 array inside. (Left, Forward, Right moves)
        move_list = snake.generateSpaceListBasedOnAvailableMoves(True)
        space_score_list = snake.generateSpaceListBasedOnAvailableMoves(False)


        for index, move in enumerate(move_list):
            final_score_list = []
            extract_space_list = []

            for i in space_score_list[index]:
                extract_space_list.append(i[1])

            if move:
                # this is to get the highest value (might bne used for smoothness, need to consider if it is supposed
                # to find the highest value or the amount of places it can go. (need consideration))
                maximum = 0
                for i in move:
                    if i[0] > maximum:
                        maximum = i[0]

                # first will be smoothness (need further thinking)
                # second will be space
                # third will be foodMoveEval
                final_score_list.append()
                final_score_list.append(len(space_score_list[index]))
                final_score_list.append(self.foodMoveEvaluation(space_score_list[index][0][1], extract_space_list, food, move[0][1]))
            else:
                final_score_list.append(0)
            final_scores.append(final_score_list)

        final_score = max(final_scores)
        return final_scores.index(final_score), final_score

    def __init__(self, w=640, h=480):
        pg.init()

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

        # testing

        # setup the player/AI objects (all takes the first part of the algorithm to have the same body and food position)
        a_star = AStar()
        a_star_food = Food(a_star.body)

        best_first_search_plus = BestFirstSearchPlus()
        random_search_plus = RandomSearchPlus()
        almighty_move = AlmightyMove()

        self.update_other_algo(a_star, best_first_search_plus, random_search_plus, almighty_move)

        best_first_search_plus_food = Food(best_first_search_plus.body)
        random_search_plus_food = Food(random_search_plus.body)
        almighty_move_food = Food(almighty_move.body)

        self.update_other_food(a_star_food, almighty_move_food, best_first_search_plus_food, random_search_plus_food)

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

                if not a_star.defeated and not found_solution:
                    if not a_star.path:
                        a_star.getPath(a_star_food)

                    if a_star.path:
                        a_star.move(a_star_food)
                    if drawing(SA3, a_star, a_star_food, squareSizeSide):
                        print("a-star")
                        found_solution = True
                        self.update_other_algo(a_star, best_first_search_plus, random_search_plus, almighty_move)
                        self.update_other_food(a_star_food, best_first_search_plus_food, random_search_plus_food,
                                               almighty_move_food)
                        print(len(a_star.body), len(best_first_search_plus.body), len(almighty_move.body),
                              len(random_search_plus.body))
                        a_star.path = []

                if not best_first_search_plus.defeated and not found_solution:
                    best_first_search_plus.move(best_first_search_plus_food)
                    if drawing(SA1, best_first_search_plus, best_first_search_plus_food, squareSizeSide):
                        print("best first search")
                        found_solution = True
                        self.update_other_algo(best_first_search_plus, a_star, random_search_plus, almighty_move)
                        self.update_other_food(best_first_search_plus_food, a_star_food, random_search_plus_food,
                                               almighty_move_food)
                        print(len(a_star.body), len(best_first_search_plus.body), len(almighty_move.body),
                              len(random_search_plus.body))
                        a_star.path = []

                if not random_search_plus.defeated and not found_solution:
                    random_search_plus.move(random_search_plus_food)
                    if drawing(SA5, random_search_plus, random_search_plus_food, squareSizeSide):
                        print("random search")
                        found_solution = True
                        self.update_other_algo(random_search_plus, best_first_search_plus, a_star, almighty_move)
                        self.update_other_food(random_search_plus_food, best_first_search_plus_food, a_star_food,
                                               almighty_move_food)
                        print(len(a_star.body), len(best_first_search_plus.body), len(almighty_move.body),
                              len(random_search_plus.body))
                        a_star.path = []

                if not almighty_move.defeated and not found_solution:
                    almighty_move.move(almighty_move_food)
                    if drawing(SA4, almighty_move, almighty_move_food, squareSizeSide):
                        print("almight")
                        self.update_other_algo(almighty_move, best_first_search_plus, random_search_plus, a_star)
                        self.update_other_food(almighty_move_food, best_first_search_plus_food, random_search_plus_food,
                                               a_star_food)
                        print(len(a_star.body), len(best_first_search_plus.body), len(almighty_move.body),
                              len(random_search_plus.body))
                        a_star.path = []

                if almighty_move.defeated and random_search_plus.defeated and a_star.defeated and best_first_search_plus.defeated:
                    print("g")
                    self.update_other_algo(a_star, best_first_search_plus, random_search_plus, almighty_move)
                    self.update_other_food(a_star_food, best_first_search_plus_food, random_search_plus_food,
                                           almighty_move_food)
                    print(len(a_star.body), len(best_first_search_plus.body), len(almighty_move.body),
                          len(random_search_plus.body))

                screen.blit(SA1, (10, 5))
                screen.blit(SA3, (50 + (boardSideSize * 2), 5))
                screen.blit(SA4, (10, boardSideSize + 10))
                screen.blit(SA5, (50 + (boardSideSize * 2), boardSideSize + 10))
                pg.display.update()

                clock.tick(SPEED)
            except KeyboardInterrupt:
                quit()
