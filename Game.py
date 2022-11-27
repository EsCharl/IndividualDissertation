import os.path

import pygame as pg

import pygame.font

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
from threading import Timer
from datetime import datetime

gameBoardColour = (20, 50, 90)
backgroundColour = (20, 40, 70)
scoreColour = (20, 40, 70)
SPEED = 10


def drawGame(canvas, snake, snake_food, square_size_side):
    score = 0
    # draw the snake on the board
    DrawSnake.DrawSnake(canvas, snake.body, square_size_side)

    if (snake.body[0][0] == snake_food.foodX) and (snake.body[0][1] == snake_food.foodY):
        score = 1
        snake_food.randomFood(snake.body)
        snake.ate = True

    # draws the food
    pg.draw.rect(canvas, (255, 0, 0),
                 pg.Rect(snake_food.foodX * square_size_side, snake_food.foodY * square_size_side,
                         square_size_side, square_size_side))

    # for score
    return score


class GameScreen:
    def drawUI(self, canvas, S1, S2, S3, S4, S5, game_board_size, time):

        score_rect_1 = self.gamer1Font.render(str(S1), True, (255, 0, 0))
        score_rect_2 = self.gamer2Font.render(str(S2), True, (255, 0, 0))
        score_rect_3 = self.gamer3Font.render(str(S3), True, (255, 0, 0))
        score_rect_4 = self.gamer4Font.render(str(S4), True, (255, 0, 0))
        score_rect_5 = self.gamer5Font.render(str(S5), True, (255, 0, 0))

        time = self.gamer5Font.render(str(int(time * 60 - (datetime.now() - self.game_start).total_seconds())), True, (255, 255, 255))

        canvas.blit(score_rect_1, (0, 0))
        canvas.blit(score_rect_2, (game_board_size / 2 - 20, 0))
        canvas.blit(score_rect_3, (game_board_size - 50, 0))
        canvas.blit(score_rect_4, (0, game_board_size - 20))
        canvas.blit(score_rect_5, (game_board_size - 50, game_board_size - 20))

        canvas.blit(time, (game_board_size/2, game_board_size/2))

    def __init__(self, w=640, h=480, time=3):
        pg.init()

        self.gamer1Font = pygame.font.SysFont('Arial', int(25 * h / 768), bold=True)
        self.gamer2Font = pygame.font.SysFont('Arial', int(25 * h / 768), bold=True)
        self.gamer3Font = pygame.font.SysFont('Arial', int(25 * h / 768), bold=True)
        self.gamer4Font = pygame.font.SysFont('Arial', int(25 * h / 768), bold=True)
        self.gamer5Font = pygame.font.SysFont('Arial', int(25 * h / 768), bold=True)
        self.timerFont = pygame.font.SysFont('Arial', int(30 * h / 768), bold=True)

        self.w = w
        self.h = h
        screen = pg.display.set_mode((self.w, self.h))
        screen.fill(backgroundColour)
        pg.display.update()
        clock = pg.time.Clock()
        all_sprites = pg.sprite.Group()

        boardSideSize = GameBoardSize.get_size(self.w)
        squareSizeSide = PixelSize.get_block_size(boardSideSize, SQUARE_AMOUNT)

        SA1 = pg.Surface((boardSideSize, boardSideSize))
        SAP = pg.Surface((boardSideSize, boardSideSize))
        SA3 = pg.Surface((boardSideSize, boardSideSize))
        SA4 = pg.Surface((boardSideSize, boardSideSize))
        SA5 = pg.Surface((boardSideSize, boardSideSize))

        UI = pg.Surface((boardSideSize, boardSideSize))

        A1Score = 0
        PScore = 0
        A3Score = 0
        A4Score = 0
        A5Score = 0

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

        self.done = False

        # this part is used to end the game after a certain amount of time.
        def gameEnd():
            self.done = True
            return

        t = Timer(time * 60, gameEnd)
        t.start()

        self.game_start = datetime.now()

        while not self.done:
            try:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.done = True
                        pg.quit()
                        t.cancel()
                        quit()

                    player.play_step(event)

                player.move()

                SA1.fill(gameBoardColour)
                SAP.fill(gameBoardColour)
                SA3.fill(gameBoardColour)
                SA4.fill(gameBoardColour)
                SA5.fill(gameBoardColour)

                UI.fill(backgroundColour)

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

                A1Score += drawGame(SA1, best_first_search, best_first_search_food, squareSizeSide)
                PScore += drawGame(SAP, player, player_food, squareSizeSide)
                A3Score += drawGame(SA3, a_star, a_star_food, squareSizeSide)
                A4Score += drawGame(SA4, almighty_move, almighty_move_food, squareSizeSide)
                A5Score += drawGame(SA5, random_search_plus, random_search_plus_food, squareSizeSide)

                screen.blit(SA1, (10, 5))
                screen.blit(SAP, (boardSideSize + 30, 5))
                screen.blit(SA3, (50 + (boardSideSize * 2), 5))
                screen.blit(SA4, (10, boardSideSize + 10))
                screen.blit(SA5, (50 + (boardSideSize * 2), boardSideSize + 10))

                # this is for the User interface (score, time)
                self.drawUI(UI, A1Score, PScore, A3Score, A4Score, A5Score, boardSideSize, time)

                screen.blit(UI, (boardSideSize + 30, boardSideSize + 10))

                pg.display.update()

                clock.tick(SPEED)

            except KeyboardInterrupt:
                t.cancel()
        else:
            print("game complete")
            game_score_saving = "Score"

            if not os.path.exists(game_score_saving):
                os.makedirs(game_score_saving)
            file_name = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            with open(game_score_saving + "/" + file_name+".txt", 'w') as f:
                f.write("Gamer 1: " + str(A1Score) + "\n")
                f.write("Gamer 2: " + str(PScore) + "\n")
                f.write("Gamer 3: " + str(A3Score) + "\n")
                f.write("Gamer 4: " + str(A4Score) + "\n")
                f.write("Gamer 5: " + str(A5Score) + "\n")


