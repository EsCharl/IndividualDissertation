import Constants
from Learning import EAEvaluation
from SnakeLogicModel import SnakeLogicModel


class Model(SnakeLogicModel):
    def __init__(self, parameters, name="Model"):
        super().__init__(name)
        self.reset()
        self.defeated = False
        self.weights = parameters

    def move(self, food):
        step = EAEvaluation.accumulationEvaluation(self, food, self.weights)
        move_coord = self.getCoordinate(step[0])

        if move_coord in self.body or move_coord[0] < 0 or move_coord[1] < 0 or \
                move_coord[0] > Constants.SQUARE_AMOUNT - 1 or move_coord[1] > Constants.SQUARE_AMOUNT - 1:
            self.reset()
            self.defeated = True
        else:
            self.body.insert(0, move_coord)
            self.checkAte(food, self.body)
            return move_coord
