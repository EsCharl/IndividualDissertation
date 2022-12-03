import pygame as pg

class DrawSnake():
    def __init__(self,surface, body, squareSizeSide):
        pg.draw.rect(surface, (0, 255, 0),
                     pg.Rect(body[0][0] * squareSizeSide, body[0][1] * squareSizeSide,
                             squareSizeSide, squareSizeSide))
        for block in body[1:]:
            pg.draw.rect(surface, (255, 255, 255),
                         pg.Rect(block[0] * squareSizeSide, block[1] * squareSizeSide,
                                 squareSizeSide, squareSizeSide))
