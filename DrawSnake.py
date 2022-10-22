import pygame as pg

class DrawSnake():
    def __init__(self,surface, body, squareSizeSide):
        for block in body:
            pg.draw.rect(surface, (255, 255, 255),
                         pg.Rect(block[0] * squareSizeSide, block[1] * squareSizeSide,
                                 squareSizeSide, squareSizeSide))
