from queue import PriorityQueue

from Constants import SQUARE_AMOUNT
from SnakeLogic import SnakeLogic


class AStar(SnakeLogic):
    def __init__(self):
        self.cost_g = 0
        self.cost_h = 0
        self.face_direction = 0
        self.possible_moves = PriorityQueue()

    def move(self):



    def availableMoves(self):
        available_moves = []
        for x in range(SQUARE_AMOUNT):
            for y in range(SQUARE_AMOUNT):
                if not [x,y] in self.body:
                    available_moves.append([x,y])

    def insert_key(self, moves, food):
        for move in moves:
            manhattan_distance = abs(move[0] - self.body[0][0]) + abs(move[1] - self.body[0][1])
            self.possible_moves.put(manhattan_distance,move)

        for x in self.possible_moves:
            if move[0] == food.foodX and move[1] == food.foodY:
                food_location = move


