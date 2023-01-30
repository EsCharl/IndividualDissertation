import random

import Constants


class SnakeLogic:

    def generateAllPotentialSteps(self, check=None):
        steps = []
        if check:
            if check[0] + 1 < Constants.SQUARE_AMOUNT:
                steps.append([check[0] + 1, check[1]])
            if check[0] - 1 >= 0:
                steps.append([check[0] - 1, check[1]])
            if check[1] + 1 < Constants.SQUARE_AMOUNT:
                steps.append([check[0], check[1] + 1])
            if check[1] - 1 >= 0:
                steps.append([check[0], check[1] - 1])
        else:
            if self.body[0][0] + 1 < Constants.SQUARE_AMOUNT:
                steps.append([self.body[0][0] + 1, self.body[0][1]])
            if self.body[0][0] - 1 >= 0:
                steps.append([self.body[0][0] - 1, self.body[0][1]])
            if self.body[0][1] + 1 < Constants.SQUARE_AMOUNT:
                steps.append([self.body[0][0], self.body[0][1] + 1])
            if self.body[0][1] - 1 >= 0:
                steps.append([self.body[0][0], self.body[0][1] - 1])
        return steps

    def checkSnake(self):
        if len(self.body) == Constants.SQUARE_AMOUNT * Constants.SQUARE_AMOUNT:
            self.reset()

        if self.body[0][0] < 0 or self.body[0][1] > Constants.SQUARE_AMOUNT - 1 or self.body[0][0] \
                > Constants.SQUARE_AMOUNT - 1 or self.body[0][1] < 0:
            self.reset()

        for x in self.body[1:]:
            if self.body[0] == x:
                self.reset()

    def reset(self):
        self.body = [[random.randint(2, Constants.SQUARE_AMOUNT - 3), random.randint(2, Constants.SQUARE_AMOUNT - 3)]]
        for x in range(0, 2):
            if random.randint(0, 1):
                self.body.append([self.body[x][0] + 1, self.body[x][1]])
            else:
                self.body.append([self.body[x][0], self.body[x][1] + 1])
        self.ate = False

    def checkAte(self, food, body):
        if not body[0] == [food.foodX, food.foodY]:
            self.body.pop()

    # this is to get the direction where it is going (adapter method)
    def getAISnakeDirection(self, body, next_step):
        # note the direction will be based on [left, forward, right]
        direction = []
        # if next_step is none
        if not next_step:
            direction = None
        else:
            forward_holder = [body[0][0] - body[1][0], body[0][1] - body[1][1]]
            forward_coordinate = [forward_holder[0] + body[0][0], body[0][1] + forward_holder[1]]

            # if snake is going forward
            if forward_coordinate == next_step:
                direction = [0, 1, 0]
            else:
                # this part is if it is going left or right.
                # if the forward is downwards.
                if forward_holder == [0, 1]:
                    # if next step is right, else left
                    if next_step == [body[0][0] - 1, body[0][1]]:
                        direction = [0, 0, 1]
                    else:
                        direction = [1, 0, 0]

                # if the forward is rightwards.
                elif forward_holder == [1, 0]:
                    # if next step is right, else left
                    if next_step == [body[0][0], body[0][1] + 1]:
                        direction = [0, 0, 1]
                    else:
                        direction = [1, 0, 0]

                # if the forward is leftwards.
                elif forward_holder == [-1, 0]:
                    # if next step is right, else left
                    if next_step == [body[0][0], body[0][1] - 1]:
                        direction = [0, 0, 1]
                    else:
                        direction = [1, 0, 0]

                # if the forward is upwards.
                elif forward_holder == [0, -1]:
                    # if next step is right, else left
                    if next_step == [body[0][0] + 1, body[0][1]]:
                        direction = [0, 0, 1]
                    else:
                        direction = [1, 0, 0]

        return direction

    # this function used to check all the possible subsequent steps available and index them based on the move index
    # formula bodyIndex + moveStep > snakeLength (taken from the paper if mode is True, default).
    # If mode is 0 (False) then it will find all space available based on its move.
    def getAllPossibleSteps(self, check_coordinate, mode=True):
        body_length = len(self.body)
        checked_index = 0

        # used to check the checked coordinates and store them
        checked_step_list = [check_coordinate]
        if mode or check_coordinate not in self.body:
            completed_all_possible_step = [[1, check_coordinate]]

            # gets all the possible moves (excluding the body)
            # Need checking
            while True:
                try:
                    holder_list = self.generateAllPotentialSteps(checked_step_list[checked_index])

                    # check the values in the possible moves
                    if mode:
                        for i in holder_list:
                            if i not in checked_step_list:
                                if i not in self.body or (i in self.body and (
                                        completed_all_possible_step[checked_index][0] + 1 + self.body.index(
                                    i) + 1) > body_length):
                                    checked_step_list.append(i)
                                    completed_all_possible_step.append(
                                        [completed_all_possible_step[checked_index][0] + 1, i])
                    else:
                        for i in holder_list:
                            if i not in checked_step_list:
                                if i not in self.body:
                                    checked_step_list.append(i)
                                    completed_all_possible_step.append(
                                        [completed_all_possible_step[checked_index][0] + 1, i])
                    checked_index += 1
                except IndexError:
                    break
        else:
            completed_all_possible_step = []
        return completed_all_possible_step

    # implement of a check space checking algorithm based on available moves.
    # this will be used for evaluation (a possibility of new algorithm might be implemented).
    def generateSpaceListBasedOnAvailableMoves(self, mode):
        final_list = []

        forward_holder = [self.body[0][0] - self.body[1][0], self.body[0][1] - self.body[1][1]]
        forward_coordinate = [forward_holder[0] + self.body[0][0], self.body[0][1] + forward_holder[1]]

        # if the forward is downwards
        if forward_holder == [0, 1]:
            # left
            if not [self.body[0][0] + 1, self.body[0][1]] in self.body and self.body[0][
                0] + 1 < Constants.SQUARE_AMOUNT:
                left_list = self.getAllPossibleSteps([self.body[0][0] + 1, self.body[0][1]], mode)
                final_list.append([left_list, len(left_list)])
            else:
                final_list.append([[], 0])

            # forward
            if forward_coordinate[0] < 0 or forward_coordinate[0] >= Constants.SQUARE_AMOUNT or forward_coordinate[
                1] < 0 or forward_coordinate[1] >= Constants.SQUARE_AMOUNT:
                final_list.append([[], 0])
            elif forward_coordinate not in self.body:
                forward_list = self.getAllPossibleSteps(forward_coordinate, mode)
                final_list.append([forward_list, len(forward_list)])
            else:
                final_list.append([[], 0])

            # right
            if not [self.body[0][0] - 1, self.body[0][1]] in self.body and self.body[0][0] - 1 >= 0:
                right_list = self.getAllPossibleSteps([self.body[0][0] - 1, self.body[0][1]], mode)
                final_list.append([right_list, len(right_list)])
            else:
                final_list.append([[], 0])

        # if the forward is upwards.
        elif forward_holder == [0, -1]:
            # left
            if not [self.body[0][0] - 1, self.body[0][1]] in self.body and self.body[0][0] - 1 >= 0:
                left_list = self.getAllPossibleSteps([self.body[0][0] - 1, self.body[0][1]], mode)
                final_list.append([left_list, len(left_list)])
            else:
                final_list.append([[], 0])

            # forward
            if forward_coordinate[0] < 0 or forward_coordinate[0] >= Constants.SQUARE_AMOUNT or forward_coordinate[
                1] < 0 or forward_coordinate[1] >= Constants.SQUARE_AMOUNT:
                final_list.append([[], 0])
            elif forward_coordinate not in self.body:
                forward_list = self.getAllPossibleSteps(forward_coordinate, mode)
                final_list.append([forward_list, len(forward_list)])
            else:
                final_list.append([[], 0])

            # right
            if not [self.body[0][0] + 1, self.body[0][1]] in self.body and self.body[0][
                0] + 1 < Constants.SQUARE_AMOUNT:
                right_list = self.getAllPossibleSteps([self.body[0][0] + 1, self.body[0][1]], mode)
                final_list.append([right_list, len(right_list)])
            else:
                final_list.append([[], 0])

        # if the forward is rightwards.
        elif forward_holder == [1, 0]:
            # left
            if not [self.body[0][0], self.body[0][1] - 1] in self.body and self.body[0][1] - 1 >= 0:
                left_list = self.getAllPossibleSteps([self.body[0][0], self.body[0][1] - 1], mode)
                final_list.append([left_list, len(left_list)])
            else:
                final_list.append([[], 0])

            # forward
            if forward_coordinate[0] < 0 or forward_coordinate[0] >= Constants.SQUARE_AMOUNT or forward_coordinate[
                1] < 0 or forward_coordinate[1] >= Constants.SQUARE_AMOUNT:
                final_list.append([[], 0])
            elif forward_coordinate not in self.body:
                forward_list = self.getAllPossibleSteps(forward_coordinate, mode)
                final_list.append([forward_list, len(forward_list)])
            else:
                final_list.append([[], 0])

            # right
            if not [self.body[0][0], self.body[0][1] + 1] in self.body and self.body[0][
                1] + 1 < Constants.SQUARE_AMOUNT:
                right_list = self.getAllPossibleSteps([self.body[0][0], self.body[0][1] + 1], mode)
                final_list.append([right_list, len(right_list)])
            else:
                final_list.append([[], 0])

        # if the forward is leftwards.
        elif forward_holder == [-1, 0]:
            # left
            if not [self.body[0][0], self.body[0][1] + 1] in self.body and self.body[0][
                1] + 1 < Constants.SQUARE_AMOUNT:
                left_list = self.getAllPossibleSteps([self.body[0][0], self.body[0][1] + 1], mode)
                final_list.append([left_list, len(left_list)])
            else:
                final_list.append([[], 0])

            # forward
            if forward_coordinate[0] < 0 or forward_coordinate[0] >= Constants.SQUARE_AMOUNT or forward_coordinate[
                1] < 0 or forward_coordinate[1] >= Constants.SQUARE_AMOUNT:
                final_list.append([[], 0])
            elif forward_coordinate not in self.body:
                forward_list = self.getAllPossibleSteps(forward_coordinate, mode)
                final_list.append([forward_list, len(forward_list)])
            else:
                final_list.append([[], 0])

            # right
            if not [self.body[0][0], self.body[0][1] - 1] in self.body and self.body[0][1] - 1 >= 0:
                right_list = self.getAllPossibleSteps([self.body[0][0], self.body[0][1] - 1], mode)
                final_list.append([right_list, len(right_list)])
            else:
                final_list.append([[], 0])

        return final_list
