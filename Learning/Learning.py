import pygame as pg

import GameBoardSize

gameBoardColour = (100, 50, 90)

class LearningScreen:
    def __init__(self,w=640,h=480):
        pg.init()

        self.w = w
        self.h = h
        screen = pg.display.set_mode((self.w, self.h))
        screen.fill((20, 40, 100))
        pg.display.update()
        clock = pg.time.Clock()
        all_sprites = pg.sprite.Group()

        boardSideSize = GameBoardSize.get_size(self.w)

        AI1 = pg.Rect(10, 5, boardSideSize, boardSideSize)
        AI2 = pg.Rect(50 + (boardSideSize * 2), 5, boardSideSize, boardSideSize)
        AI3 = pg.Rect(10, boardSideSize + 10, boardSideSize, boardSideSize)
        AI4 = pg.Rect(50 + (boardSideSize * 2), boardSideSize + 10, boardSideSize, boardSideSize)

        done = False
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True

            # add the snake algo and snake display here

            all_sprites.update()

            screen.fill(gameBoardColour)
            all_sprites.draw(screen)

            # Update only the area that we specified with the `update_rect`.
            pg.display.update(AI1)
            pg.display.update(AI2)
            pg.display.update(AI3)
            pg.display.update(AI4)
            clock.tick(60)