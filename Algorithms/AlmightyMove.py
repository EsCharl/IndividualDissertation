from Constants import SQUARE_AMOUNT
from Directions import Directions
from SnakeLogic import SnakeLogic


class AlmightyMove(SnakeLogic):
    def __init__(self):
        self.reset()
        self.template_path_0 = []
        self.template_path_1 = []
        self.generate_template_path()

    def generate_template_path(self):
        # this is odd number game-board
        if SQUARE_AMOUNT % 2:
            # left template first
            for y in range(SQUARE_AMOUNT):
                for x in range(SQUARE_AMOUNT):
                    break
        else:
            # this is for even number game-board
            for x in range(SQUARE_AMOUNT):
                for y in range(SQUARE_AMOUNT):
                    # odd
                    if x % 2:
                        self.template_path_0.append([[x,y],Directions.DOWN])
                    # even
                    else:
                        self.template_path_0.append([[x,y],Directions.UP])

            # this part changes the direction
            for i in range(len(self.template_path_0)):
                if self.template_path_0[i][0][1] == SQUARE_AMOUNT - 1:
                    self.template_path_0[i][1] = Directions.LEFT
                elif self.template_path_0[i][0][1] == 0 and not self.template_path_0[i][0][0] % 2:
                    self.template_path_0[i][1] = Directions.RIGHT
                elif self.template_path_0[i][0][0] % 2 and self.template_path_0[i][0][1] == SQUARE_AMOUNT - 2 and not self.template_path_0[i][0][0] == SQUARE_AMOUNT - 1:
                    self.template_path_0[i][1] = Directions.RIGHT

    def reset(self):
        super(AlmightyMove, self).reset()
        self.template = 1

    def move(self):
        filtered_steps = []
        potential_steps = self.generate_all_potential_steps()

        # this filters all possible moves that the snake can make
        for x in potential_steps:
            if not (x in self.body):
                filtered_steps.append(x)

        # if the game-board is odd
        if SQUARE_AMOUNT % 2:
            if self.body[0] == [0,1]:
                if self.template:
                    self.template = 0
                else:
                    self.template = 1

        else:
            preferred_direction = None
            for i in self.template_path_0:
                if i[0] == self.body[0]:
                    preferred_direction = i[1]
                    break

            preferred_step = self.check_direction_possible(filtered_steps, preferred_direction)

            # if can't get a preferred_step
            if not preferred_step and filtered_steps:
                if self.body[0][1] < SQUARE_AMOUNT - 1 and [self.body[0][0] + 1, self.body[0][1]] in filtered_steps:
                    preferred_step = [self.body[0][0] + 1, self.body[0][1]]
                elif self.body[0][1] == SQUARE_AMOUNT - 1 and [self.body[0][0], self.body[0][1] - 1] in filtered_steps:
                    preferred_step = [self.body[0][0], self.body[0][1] - 1]

            if not preferred_step and len(filtered_steps) == 1:
                preferred_step = filtered_steps[0]
            elif not preferred_step and filtered_steps:
                if preferred_direction == Directions.DOWN:
                    preferred_direction = Directions.UP
                elif preferred_direction == Directions.UP:
                    preferred_direction = Directions.DOWN
                elif preferred_direction == Directions.LEFT:
                    preferred_direction = Directions.RIGHT
                elif preferred_direction == Directions.RIGHT:
                    preferred_direction = Directions.LEFT
                preferred_step = self.check_direction_possible(filtered_steps, preferred_direction)

            # # this parts changes the direction when it is on the bottom edges
            # if self.body[0] == [SQUARE_AMOUNT - 1, SQUARE_AMOUNT - 1] or self.body[0] == [0, SQUARE_AMOUNT - 1]:
            #     if self.vertical_direction == Directions.DOWN:
            #         self.vertical_direction = Directions.UP
            #
            # # this part changes the vertical direction when the head reaches the top row and the direction is up.
            # if self.body[0][1] == 0 and self.vertical_direction == Directions.UP:
            #     self.vertical_direction = Directions.DOWN
            # # this part changes the vertical direction when the head reaches the 2nd bottom row and the direction is down
            # elif self.body[0][1] == SQUARE_AMOUNT - 2 and self.vertical_direction == Directions.DOWN:
            #     self.vertical_direction = Directions.UP
            #
            # # this part changes the horizontal when the head reaches the furthest right, and it is on the right direction
            # if self.body[0][0] == SQUARE_AMOUNT - 1 and self.horizontal_direction == Directions.RIGHT:
            #     self.horizontal_direction = Directions.LEFT
            #
            # # this part changes the horizontal when the head reaches the furthest left, and it is on the left direction
            # if self.body[0][0] == 0 and self.horizontal_direction == Directions.LEFT:
            #     self.horizontal_direction = Directions.RIGHT
            #
            # # this part moves decide the moves for the snake
            # if self.body[0][1] == SQUARE_AMOUNT - 1 and not self.body[0][0] == 0:
            #     step = self.decide_horizontal(self.horizontal_direction)
            # elif self.body[0] == [SQUARE_AMOUNT - 1, SQUARE_AMOUNT - 2]:
            #     self.vertical_direction = Directions.DOWN
            #     step = self.decide_vertical(self.vertical_direction)
            # elif self.body[0] == [0, SQUARE_AMOUNT - 1]:
            #     step = self.decide_vertical(self.vertical_direction)
            # elif (self.body[0][1] + 1 in self.body or ((self.body[0][1] == SQUARE_AMOUNT - 2 or self.body[0][
            #     1] == 0) and not self.moved_horizontal)) and self.horizontal_direction == Directions.RIGHT:
            #     step = self.decide_horizontal(self.horizontal_direction)
            #     self.moved_horizontal = True
            # else:
            #     step = self.decide_vertical(self.vertical_direction)
            #     self.moved_horizontal = False


        # this part checks if the step being made is it require a reset.
        if preferred_step:
            print(self.body, preferred_step)
            self.body.insert(0, preferred_step)
            self.checkAte()
        else:
            print("t", self.body, preferred_step)
            self.reset()

    def check_direction_possible(self, filtered_steps, preferred_direction):
        preferred_step = None
        if preferred_direction == Directions.UP and [self.body[0][0], self.body[0][1] - 1] in filtered_steps:
            preferred_step = [self.body[0][0], self.body[0][1] - 1]
        elif preferred_direction == Directions.RIGHT and [self.body[0][0] + 1, self.body[0][1]] in filtered_steps:
            preferred_step = [self.body[0][0] + 1, self.body[0][1]]
        elif preferred_direction == Directions.LEFT and [self.body[0][0] - 1, self.body[0][1]] in filtered_steps:
            preferred_step = [self.body[0][0] - 1, self.body[0][1]]
        elif preferred_direction == Directions.DOWN and [self.body[0][0], self.body[0][1] + 1] in filtered_steps:
            preferred_step = [self.body[0][0], self.body[0][1] + 1]
        return preferred_step

    def decide_horizontal(self, direction):
        self.moved_horizontal = True
        if direction == Directions.LEFT:
            return [self.body[0][0] - 1, self.body[0][1]]
        elif direction == Directions.RIGHT:
            return [self.body[0][0] + 1, self.body[0][1]]

    def decide_vertical(self, direction):
        if direction == Directions.UP:
            return [self.body[0][0], self.body[0][1] - 1]
        elif direction == Directions.DOWN:
            return [self.body[0][0], self.body[0][1] + 1]
