import pygame
import pygame as pg

# A simple sprite, just to have something moving on the screen.
import DrawSnake
import GameBoardSize
import PixelSize
import Player
from Algorithms.AlmightyMove import AlmightyMove
from Algorithms.AStar import AStar
from Algorithms.BestFirstSearchPlus import BestFirstSearchPlus
from Algorithms.RandomSearchPlus import RandomSearchPlus
from Constants import SQUARE_AMOUNT
from Food import Food

gameBoardColour = (20, 50, 90)
SPEED = 10


def drawing(canvas, snake, snake_food, square_size_side):
    DrawSnake.DrawSnake(canvas, snake.body, square_size_side)

    if (snake.body[0][0] == snake_food.foodX) and (snake.body[0][1] == snake_food.foodY):
        snake_food.randomFood(snake.body)
        snake.ate = True

    pg.draw.rect(canvas, (255, 0, 0),
                 pg.Rect(snake_food.foodX * square_size_side, snake_food.foodY * square_size_side,
                         square_size_side, square_size_side))


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
        squareSizeSide = PixelSize.get_block_size(boardSideSize, SQUARE_AMOUNT)

        SA1 = pygame.Surface((boardSideSize, boardSideSize))
        SAP = pygame.Surface((boardSideSize, boardSideSize))
        SA3 = pygame.Surface((boardSideSize, boardSideSize))
        SA4 = pygame.Surface((boardSideSize, boardSideSize))
        SA5 = pygame.Surface((boardSideSize, boardSideSize))

        # testing

        # setup the player/AI objects
        player = Player.Player()
        player_food = Food(player.body)

        a_star = AStar()
        a_star_food = Food(a_star.body)

        best_first_search = BestFirstSearchPlus()
        best_first_search_food = Food(best_first_search.body)

        random_search_plus = RandomSearchPlus()
        random_search_plus_food = Food(random_search_plus.body)

        almighty_move = AlmightyMove()
        almighty_move_food = Food(almighty_move.body)

        done = False
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                    pygame.quit()
                    quit()

                player.play_step(event)

            player.move()

            SA1.fill(gameBoardColour)
            SAP.fill(gameBoardColour)
            SA3.fill(gameBoardColour)
            SA4.fill(gameBoardColour)
            SA5.fill(gameBoardColour)

            all_sprites.update()

            all_sprites.draw(screen)

            if not a_star.path:
                a_star.getPath(a_star_food)

            player.checkAte()
            player.checkSnake()

            # best_first_search.checkSnake()
            # random_search_plus.checkSnake()
            # a_star.checkSnake()

            a_star.move()

            best_first_search.move(best_first_search_food)
            random_search_plus.move()
            almighty_move.move()

            drawing(SA3, a_star, a_star_food, squareSizeSide)
            drawing(SA5, random_search_plus, random_search_plus_food, squareSizeSide)
            drawing(SA4, almighty_move, almighty_move_food, squareSizeSide)
            drawing(SA1, best_first_search, best_first_search_food, squareSizeSide)
            drawing(SAP, player, player_food, squareSizeSide)

            screen.blit(SA1, (10, 5))
            screen.blit(SAP, (boardSideSize + 30, 5))
            screen.blit(SA3, (50 + (boardSideSize * 2), 5))
            screen.blit(SA4, (10, boardSideSize + 10))
            screen.blit(SA5, (50 + (boardSideSize * 2), boardSideSize + 10))
            pg.display.update()

            clock.tick(SPEED)
