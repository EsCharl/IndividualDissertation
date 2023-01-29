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

    # implement of a check space checking algorithm based on available moves.
    # (note to self: store into an array, further brainstorming on how to store it will be needed).
    # this will be used for evaluation (a possibility of new algorithm might be implemented).
    def generateSpaceListBasedOnAvailableMoves(self, set_body):
        body_length = len(self.body)
        final_list = []

        # issue: computationally expensive (need to compare two list to check for coordinates checked). can't use set.
        # can't add list into sets
        def getAllPossibleSteps(check_coordinate):

            return

        forward_holder = [self.body[0][0] - self.body[1][0], self.body[0][1] - self.body[1][1]]
        forward_coordinate = [forward_holder[0] + self.body[0][0], self.body[0][1] + forward_holder[1]]

        set_body = set(self.body)
        # if the forward is downwards
        if forward_holder == [0, 1]:
            # left
            if not [self.body[0][0] + 1, self.body[0][1]] in set_body:
                final_list.append(getAllPossibleSteps([self.body[0][0] + 1, self.body[0][1]]))
            # forward
            if not (forward_coordinate in set_body):
                final_list.append(getAllPossibleSteps(forward_coordinate))
            # right
            if not [self.body[0][0] - 1, self.body[0][1]] in set_body:
                final_list.append(getAllPossibleSteps([self.body[0][0] - 1, self.body[0][1]]))

        # if the forward is rightwards.
        elif forward_holder == [1, 0]:
            # left
            if not [self.body[0][0], self.body[0][1] - 1] in set_body:
                final_list.append(getAllPossibleSteps([self.body[0][0], self.body[0][1] - 1]))
            # forward
            if not (forward_coordinate in set_body):
                final_list.append(getAllPossibleSteps(forward_coordinate))
            # right
            if not [self.body[0][0], self.body[0][1] + 1] in set_body:
                final_list.append(getAllPossibleSteps([self.body[0][0], self.body[0][1] + 1]))

        # if the forward is leftwards.
        elif forward_holder == [-1, 0]:
            # left
            if not [self.body[0][0], self.body[0][1] + 1] in set_body:
                final_list.append(getAllPossibleSteps([self.body[0][0], self.body[0][1] + 1]))
            # forward
            if not (forward_coordinate in set_body):
                final_list.append(getAllPossibleSteps(forward_coordinate))
            # right
            if not [self.body[0][0], self.body[0][1] - 1] in set_body:
                final_list.append(getAllPossibleSteps([self.body[0][0], self.body[0][1] - 1]))

        # if the forward is upwards.
        elif forward_holder == [0, -1]:
            # left
            if not [self.body[0][0] - 1, self.body[0][1]] in set_body:
                final_list.append(getAllPossibleSteps([self.body[0][0] - 1, self.body[0][1]]))
            # forward
            if not (forward_coordinate in set_body):
                final_list.append(getAllPossibleSteps(forward_coordinate))
            # right
            if not [self.body[0][0] + 1, self.body[0][1]] in set_body:
                final_list.append(getAllPossibleSteps([self.body[0][0] + 1, self.body[0][1]]))

        return final_list
