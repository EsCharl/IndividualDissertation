import random

import pygame
import pygame as pg

# A simple sprite, just to have something moving on the screen.
import Algorithms.BestFirstSearch
import DrawSnake
import GameBoardSize
import PixelSize
import Player
from Constants import squareAmount
from Directions import Directions
from Food import Food

gameBoardColour = (20, 50, 90)
SPEED = 10

class GameScreen:
    def __init__(self, w=640, h=480, time=3):
        pg.init()

        self.w = w
        self.h = h
        screen = pg.display.set_mode((self.w, self.h))
        screen.fill((20, 40, 70))
        pg.display.update()
        clock = pg.time.Clock()
        all_sprites = pg.sprite.Group()

        boardSideSize = GameBoardSize.get_size(self.w)
        squareSizeSide = PixelSize.get_block_size(boardSideSize,squareAmount)

        SA1 = pygame.Surface((boardSideSize,boardSideSize))
        SAP = pygame.Surface((boardSideSize,boardSideSize))
        SA3 = pygame.Surface((boardSideSize,boardSideSize))
        SA4 = pygame.Surface((boardSideSize,boardSideSize))
        SA5 = pygame.Surface((boardSideSize,boardSideSize))


        # AI1 = pg.Rect(10, 5, boardSideSize, boardSideSize)
        # player = pg.Rect(boardSideSize+30, 5, boardSideSize, boardSideSize)
        # AI3 = pg.Rect(50 + (boardSideSize * 2), 5, boardSideSize, boardSideSize)
        # AI4 = pg.Rect(10, boardSideSize + 10, boardSideSize, boardSideSize)
        # AI5 = pg.Rect(50 + (boardSideSize * 2), boardSideSize + 10, boardSideSize, boardSideSize)

        # testing
        player_snake = [[1,1],[1,2],[1,3]]


        # setup the player/AI objects
        player = Player.Player()
        player_food = Food()

        best_first_search = Algorithms.BestFirstSearch.BestFirstSearch()
        best_first_search_food = Food()

        done = False
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                    pygame.quit()
                    quit()

                direction = player.play_step(event)

            if direction == Directions.LEFT:
                player_snake.insert(0, [player_snake[0][0] - 1, player_snake[0][1]])
            elif direction == Directions.RIGHT:
                player_snake.insert(0, [player_snake[0][0] + 1, player_snake[0][1]])
            elif direction == Directions.UP:
                player_snake.insert(0, [player_snake[0][0], player_snake[0][1] - 1])
            else:
                player_snake.insert(0, [player_snake[0][0], player_snake[0][1] + 1])

            player_snake.pop()

            SA1.fill(gameBoardColour)
            SAP.fill(gameBoardColour)
            SA3.fill(gameBoardColour)
            SA4.fill(gameBoardColour)
            SA5.fill(gameBoardColour)

            all_sprites.update()

            all_sprites.draw(screen)

            best_first_search.body = best_first_search.move(best_first_search.body, best_first_search_food)

            if best_first_search.body[0][0] < 0 or best_first_search.body[0][1] > 14 or best_first_search.body[0][0] > 14 or best_first_search.body[0][1] < 0:
                best_first_search.reset()

            for block in best_first_search.body:
                DrawSnake.DrawSnake(SA1, block, squareSizeSide)

            if ((best_first_search.body[0][0] == best_first_search_food.foodX) and (best_first_search.body[0][1] == best_first_search_food.foodY)):
                best_first_search_food.randomFood()
                best_first_search.ate = True

            pg.draw.rect(SA1, (255, 0, 0),
                         pg.Rect(best_first_search_food.foodX * squareSizeSide, best_first_search_food.foodY * squareSizeSide,
                                 squareSizeSide, squareSizeSide))

            for block in player_snake:
                DrawSnake.DrawSnake(SAP, block, squareSizeSide)

            # Might need to change when the food is spawn in the snake. (further development needed)
            if ((player_snake[0][0] == player_food.foodX) and (player_snake[0][1] == player_food.foodY)):
                player_food.randomFood()

            pg.draw.rect(SAP, (255, 0, 0),
                         pg.Rect(player_food.foodX * squareSizeSide, player_food.foodY * squareSizeSide,
                                 squareSizeSide, squareSizeSide))

            screen.blit(SA1, (10,5))
            screen.blit(SAP, (boardSideSize+30, 5))
            screen.blit(SA3, (50 + (boardSideSize * 2), 5))
            screen.blit(SA4, (10, boardSideSize + 10))
            screen.blit(SA5, (50 + (boardSideSize * 2), boardSideSize + 10))
            pg.display.update()
            # pg.display.update(AI1)
            # pg.display.update(player)
            # pg.display.update(AI3)
            # pg.display.update(AI4)
            # pg.display.update(AI5)

            clock.tick(SPEED)
