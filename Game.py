import pygame
import pygame as pg

# A simple sprite, just to have something moving on the screen.
import DrawSnake
import GameBoardSize
import PixelSize

gameBoardColour = (20, 50, 90)
squareAmount = 15

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

        SA1.fill(gameBoardColour)
        SAP.fill(gameBoardColour)
        SA3.fill(gameBoardColour)
        SA4.fill(gameBoardColour)
        SA5.fill(gameBoardColour)

        # AI1 = pg.Rect(10, 5, boardSideSize, boardSideSize)
        # player = pg.Rect(boardSideSize+30, 5, boardSideSize, boardSideSize)
        # AI3 = pg.Rect(50 + (boardSideSize * 2), 5, boardSideSize, boardSideSize)
        # AI4 = pg.Rect(10, boardSideSize + 10, boardSideSize, boardSideSize)
        # AI5 = pg.Rect(50 + (boardSideSize * 2), boardSideSize + 10, boardSideSize, boardSideSize)

        # testing
        s = [[0,1],[1,2],[1,3]]
        d = [[1,1],[1,2],[1,3]]

        done = False
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True

            all_sprites.update()

            all_sprites.draw(screen)

            for block in s:
                DrawSnake.DrawSnake(SA1, block, squareSizeSide)

            for block in d:
                DrawSnake.DrawSnake(SAP, block, squareSizeSide)

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

            # add the snake algo and snake display here
            clock.tick(60)
