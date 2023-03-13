import Constants
from Learning import EAEvaluation
from SnakeLogic import SnakeLogic


class Model(SnakeLogic):
    def __init__(self, parameters, name="Model"):
        super().__init__(name)
        self.reset()
        self.defeated = False
        self.weights = parameters

    def getCoordinate(self, step):

        forward_holder = [self.body[0][0] - self.body[1][0], self.body[0][1] - self.body[1][1]]
        forward = [forward_holder[0] + self.body[0][0], self.body[0][1] + forward_holder[1]]

        # if the forward is downwards
        if forward_holder == [0, 1]:
            # left
            if step == 0:
                return [self.body[0][0] + 1, self.body[0][1]]
            elif step == 1:
                return forward
            else:
                return [self.body[0][0] - 1, self.body[0][1]]

        # if the forward is upwards.
        elif forward_holder == [0, -1]:
            # left
            if step == 0:
                return [self.body[0][0] - 1, self.body[0][1]]
            elif step == 1:
                return forward
            # right
            else:
                return [self.body[0][0] + 1, self.body[0][1]]

        # if the forward is rightwards.
        elif forward_holder == [1, 0]:
            # left
            if step == 0:
                return [self.body[0][0], self.body[0][1] - 1]
            elif step == 1:
                return forward
            # right
            else:
                return [self.body[0][0], self.body[0][1] + 1]

        # if the forward is leftwards.
        elif forward_holder == [-1, 0]:
            # left
            if step == 0:
                return [self.body[0][0], self.body[0][1] + 1]
            elif step == 1:
                return forward
            # right
            else:
                return [self.body[0][0], self.body[0][1] - 1]

    def move(self, food):
        step = EAEvaluation.accumulationEvaluation(self, food, self.weights)
        move_coord = self.getCoordinate(step[0])

        if move_coord in self.body or move_coord[0] < 0 or move_coord[1] < 0 or move_coord[0] or \
                move_coord[0] > Constants.SQUARE_AMOUNT - 1 or move_coord[1] > Constants.SQUARE_AMOUNT - 1:
            self.reset()
            self.defeated = True
        else:
            self.body.insert(0, move_coord)
            self.checkAte(food, self.body)
            return move_coord
