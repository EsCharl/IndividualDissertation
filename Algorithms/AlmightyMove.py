from Constants import SQUARE_AMOUNT
from Directions import Directions
from SnakeLogic import SnakeLogic


class AlmightyMove(SnakeLogic):
    def __init__(self):
        self.reset()

    def reset(self):
        super(AlmightyMove, self).reset()
        self.moved_horizontal = False
        if self.body[0][1] / 2 < SQUARE_AMOUNT / 2:
            self.vertical_direction = Directions.DOWN
        else:
            self.vertical_direction = Directions.UP
        if self.body[0][0] / 2 < SQUARE_AMOUNT / 2:
            self.horizontal_direction = Directions.RIGHT
        else:
            self.horizontal_direction = Directions.LEFT

    # def move(self):
    #     step = None
    #
    #     # this part deals with the vertical directions inside the inner border.
    #     if 1 < self.body[0][0] < SQUARE_AMOUNT - 2 and 1 < self.body[0][1] < SQUARE_AMOUNT - 2:
    #         if self.vertical_direction == Directions.DOWN and (self.body[0][1] + 1 in self.body or self.body[0][1] == SQUARE_AMOUNT - 2):
    #             self.vertical_direction = Directions.UP
    #         elif self.vertical_direction == Directions.UP and (self.body[0][1] - 1 in self.body or self.body[0][1] == 1):
    #             self.vertical_direction = Directions.DOWN
    #
    #     # this part deals with setting the directions (horizontal)
    #     if self.horizontal_direction == Directions.RIGHT and (self.body[0][0] == SQUARE_AMOUNT - 1):
    #         self.horizontal_direction = Directions.LEFT
    #     elif self.horizontal_direction == Directions.LEFT and (self.body[0][0] == 0):
    #         self.horizontal_direction = Directions.RIGHT
    #
    #     # this part handles the corners (vertical)
    #     if self.body[0] == [0, 0] or self.body[0] == [SQUARE_AMOUNT - 1, SQUARE_AMOUNT - 1] or self.body[0] == [SQUARE_AMOUNT - 1, 0] or self.body[0] == [0, SQUARE_AMOUNT - 1]:
    #         if self.vertical_direction == Directions.UP:
    #             self.vertical_direction = Directions.DOWN
    #         else:
    #             self.vertical_direction = Directions.UP
    #
    #     if self.body[0][]

    def move(self):
        filtered_steps = []
        potential_steps = self.generate_all_potential_steps()

        # this filters all possible moves that the snake can make
        for x in potential_steps:
            if not (x in self.body):
                filtered_steps.append(x)

        # if the game-board is odd
        if SQUARE_AMOUNT % 2:
            template = True
            if template:
                if self.body == [1, 0]:
                    if template:
                        template = False
                    else:
                        template = True

        else:
            # this parts changes the direction when it is on the bottom edges
            if self.body[0] == [SQUARE_AMOUNT - 1, SQUARE_AMOUNT - 1] or self.body[0] == [0, SQUARE_AMOUNT - 1]:
                if self.vertical_direction == Directions.DOWN:
                    self.vertical_direction = Directions.UP

            # this part changes the vertical direction when the head reaches the top row and the direction is up.
            if self.body[0][1] == 0 and self.vertical_direction == Directions.UP:
                self.vertical_direction = Directions.DOWN
            # this part changes the vertical direction when the head reaches the 2nd bottom row and the direction is down
            elif self.body[0][1] == SQUARE_AMOUNT - 2 and self.vertical_direction == Directions.DOWN:
                self.vertical_direction = Directions.UP

            # this part changes the horizontal when the head reaches the furthest right, and it is on the right direction
            if self.body[0][0] == SQUARE_AMOUNT - 1 and self.horizontal_direction == Directions.RIGHT:
                self.horizontal_direction = Directions.LEFT

            # this part changes the horizontal when the head reaches the furthest left, and it is on the left direction
            if self.body[0][0] == 0 and self.horizontal_direction == Directions.LEFT:
                self.horizontal_direction = Directions.RIGHT

            if self.body[0][1] + 1 in self.body and self.horizontal_direction == Directions.RIGHT:
                step = self.decide_horizontal(self.horizontal_direction)
            else:
                step = self.decide_vertical(self.vertical_direction)

        # this part checks if the step being made is it require a reset.
        if step[0] > SQUARE_AMOUNT - 1 or step[1] > SQUARE_AMOUNT - 1 or step[0] < 0 or step[1] < 1 or step in self.body:
            print("t", self.body, step)
            self.reset()
        else:
            print(self.body, step)
            self.body.insert(0, step)
            self.checkAte()

    def decide_horizontal(self, direction):
        self.moved_horizontal = True
        if direction == Directions.LEFT:
            return [self.body[0][0] - 1, self.body[0][1]]
        else:
            return [self.body[0][0] + 1, self.body[0][1]]


    def decide_vertical(self, direction):
        if direction == Directions.UP:
            return [self.body[0][0], self.body[0][1] - 1]
        else:
            return [self.body[0][0], self.body[0][1] + 1]