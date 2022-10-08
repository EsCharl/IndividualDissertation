import pygame as pg

import GameBoardSize
import PixelSize

pg.init()

gameBoardColour = (20, 50, 90)

class Rect(pg.sprite.Sprite):
    def __init__(self,x,y,width,height,color):
        super().__init__()
        self.image = pg.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class GameScreen:
    def __init__(self, w=640, h=480, time = 3):
        self.w = w
        self.h = h
        self.time = time

        self.display = pg.display.set_mode((self.w, self.h))
        color = (150, 150, 150)
        pg.display.set_caption('Snake Game')


        self.display.fill(color)

        boardSideSize = GameBoardSize.get_size(self.w)
        blockSideSize = PixelSize.get_block_size(boardSideSize)

        AI1 = pg.Rect(0,0,boardSideSize,boardSideSize)
        self.display.fill(gameBoardColour)
        player = pg.Rect(boardSideSize,0,boardSideSize,boardSideSize)
        self.display.fill(gameBoardColour)
        AI3 = pg.Rect(boardSideSize*2,0,boardSideSize,boardSideSize)
        self.display.fill(gameBoardColour)
        AI4 = pg.Rect(self.w / 4, boardSideSize,boardSideSize,boardSideSize)
        self.display.fill(gameBoardColour)
        AI5 = pg.Rect(self.w / 4 * 3, boardSideSize, boardSideSize,boardSideSize)
        self.display.fill(gameBoardColour)

        while True:
            pg.display.update(AI1)
            pg.display.update(player)
            pg.display.update(AI3)
            pg.display.update(AI4)
            pg.display.update(AI5)

