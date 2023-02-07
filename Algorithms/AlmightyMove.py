import random

from Constants import SQUARE_AMOUNT
from Directions import Directions
from SnakeLogic import SnakeLogic


class AlmightyMove(SnakeLogic):
    def __init__(self, name="Almighty Move"):
        super().__init__(name)
        self.reset()
        self.template_path_0 = []
        self.template_path_1 = []
        self.generate_template_path()
        self.defeated = False

    def reset(self):
        super(AlmightyMove, self).reset()
        self.template = 1

    def generate_template_path(self):
        # this is odd number game-board
        if SQUARE_AMOUNT % 2:
            # left template
            for y in range(SQUARE_AMOUNT):
                for x in range(SQUARE_AMOUNT - 1):
                    if x % 2:
                        self.template_path_0.append([[x, y], Directions.DOWN])
                    else:
                        self.template_path_0.append([[x, y], Directions.UP])

            for i in self.template_path_0.copy():
                # this part removes the top part (other than x = 0,1)
                if i[0] == [0, SQUARE_AMOUNT]:
                    i[1] = Directions.UP
                elif i[0] == [0, 0]:
                    i[1] = Directions.RIGHT
                elif i[0][1] == SQUARE_AMOUNT - 1 and not i[0] == [0, SQUARE_AMOUNT-1]:
                    i[1] = Directions.LEFT
                elif i[0][0] % 2 and i[0][1] == SQUARE_AMOUNT - 2 and not i[0] == [SQUARE_AMOUNT-2, SQUARE_AMOUNT-2]:
                    i[1] = Directions.RIGHT
                elif not i[0][0] % 2 and i[0][1] == 1 and not i[0] == [0, 1]:
                    i[1] = Directions.RIGHT
                elif i[0][0] in range(2, SQUARE_AMOUNT-1) and i[0][1] == 0:
                    self.template_path_0.remove(i)

            # right template
            for y in range(SQUARE_AMOUNT):
                for x in range(1, SQUARE_AMOUNT):
                    if x % 2:
                        self.template_path_1.append([[x, y], Directions.DOWN])
                    else:
                        self.template_path_1.append([[x, y], Directions.UP])

            for i in self.template_path_1.copy():
                if i[0] == [SQUARE_AMOUNT - 2, SQUARE_AMOUNT - 1]:
                    i[1] = Directions.RIGHT
                if i[0] == [1, 0]:
                    i[1] = Directions.DOWN
                elif i[0][1] == 0:
                    i[1] = Directions.LEFT
                elif i[0][1] == 1 and i[0][0] < SQUARE_AMOUNT - 1 and not i[0][0] % 2:
                    i[1] = Directions.RIGHT
                elif i[0][1] == SQUARE_AMOUNT - 2 and i[0][0] % 2 and not i[0] == [SQUARE_AMOUNT - 2, SQUARE_AMOUNT - 2]:
                    i[1] = Directions.RIGHT
                elif i[0][0] in range(1, SQUARE_AMOUNT - 2) and i[0][1] == SQUARE_AMOUNT - 1:
                    self.template_path_1.remove(i)

        else:
            # this is for even number game-board
            for x in range(SQUARE_AMOUNT):
                for y in range(SQUARE_AMOUNT):
                    # odd
                    if x % 2:
                        self.template_path_0.append([[x, y], Directions.DOWN])
                    # even
                    else:
                        self.template_path_0.append([[x, y], Directions.UP])

            # this part changes the direction
            for i in self.template_path_0:
                if i[0][1] == SQUARE_AMOUNT - 1 and not i[0] == [0, SQUARE_AMOUNT - 1]:
                    i[1] = Directions.LEFT
                elif i[0][1] == 0 and not i[0][0] % 2:
                    i[1] = Directions.RIGHT
                elif i[0][0] % 2 and i[0][1] == SQUARE_AMOUNT - 2 and not i[0] == [SQUARE_AMOUNT - 1, SQUARE_AMOUNT - 2]:
                    i[1] = Directions.RIGHT

    def move(self, food):
        preferred_direction = None
        filtered_steps = []
        potential_steps = self.generateAllPotentialSteps()

        # this filters all possible moves that the snake can make
        for x in potential_steps:
            if not (x in self.body):
                filtered_steps.append(x)

        # if the game-board is odd
        if SQUARE_AMOUNT % 2:

            # this is to switch the template
            if self.body[0] == [1, 0]:
                if self.template:
                    self.template = 0
                else:
                    self.template = 1

            if self.template:
                for i in self.template_path_1:
                    if i[0] == self.body[0]:
                        preferred_direction = i[1]
                        break

            else:
                for i in self.template_path_0:
                    if i[0] == self.body[0]:
                        preferred_direction = i[1]
                        break

            preferred_step = self.check_direction_possible(filtered_steps, preferred_direction)

            ## needs adding changing

            # if can't get a preferred_step (might need to consider changing the template if the snake gone to another template path.)
            if not preferred_step and filtered_steps:
                # if self.body[0][1] > 0 and [self.body[0][0] - 1, self.body[0][1]] in filtered_steps and self.template == 0:
                #     preferred_step = [self.body[0][0] - 1, self.body[0][1]]
                if self.body[0][1] < SQUARE_AMOUNT - 1 and [self.body[0][0] + 1, self.body[0][1]] in filtered_steps:
                    preferred_step = [self.body[0][0] + 1, self.body[0][1]]
                # this is for if the snake is supposed to go right, but it is blocked it will go down
                elif preferred_direction == Directions.RIGHT and [self.body[0][0], self.body[0][1] + 1] in filtered_steps:
                    preferred_step = [self.body[0][0], self.body[0][1] + 1]

            # if there is only 1 choice left.
            if not preferred_step and len(filtered_steps) == 1:
                preferred_step = filtered_steps[0]
            # this part is used to get the opposite direction where it is preferred (worse case)
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

            # this is just in case it can't find any steps (catcher)
            if not preferred_step and filtered_steps:
                preferred_step = random.choice(filtered_steps)

        else:
            for i in self.template_path_0:
                if i[0] == self.body[0]:
                    preferred_direction = i[1]
                    break

            preferred_step = self.check_direction_possible(filtered_steps, preferred_direction)

            # if can't get a preferred_step
            if not preferred_step and filtered_steps:
                if self.body[0][1] < SQUARE_AMOUNT - 1 and [self.body[0][0] + 1, self.body[0][1]] in filtered_steps:
                    preferred_step = [self.body[0][0] + 1, self.body[0][1]]

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

            # this is just in case it can't find any steps
            if not preferred_step and filtered_steps:
                preferred_step = random.choice(filtered_steps)

        # this part checks if the step being made is it require a reset.
        if preferred_step:
            # print(self.body, preferred_step)
            # print(self.getAISnakeDirection(self.body, preferred_step))
            # print(self.generateSpaceListBasedOnAvailableMoves())
            # print()
            # print(self.generateSpaceListBasedOnAvailableMoves(False)[0])
            self.body.insert(0, preferred_step)
            self.checkAte(food, self.body)
            return preferred_step
        else:
            # print("t", self.body, preferred_step)
            self.reset()
            self.defeated = True

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
