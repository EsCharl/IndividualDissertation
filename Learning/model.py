import Constants
from Learning import EAEvaluation
from SnakeLogicModel import SnakeLogicModel


class Agent(SnakeLogicModel):
    def __init__(self, weights):
        super().__init__("Generated model")
        self.score = 0
        self.reset()
        self.weights = weights

    def checkSnake(self):
        if self.body[0][0] < 0 or self.body[0][1] > Constants.SQUARE_AMOUNT - 1 or self.body[0][0] \
                > Constants.SQUARE_AMOUNT - 1 or self.body[0][1] < 0:
            return True

        for x in self.body[1:]:
            if self.body[0] == x:
                return True

        return False

    def move(self, snake, food):
        step = EAEvaluation.accumulationEvaluation(snake, food, self.weights)

        # step[0] is the index on where to go (left, forward, right)
        move_coord = self.getCoordinate(step[0])

        # need to check if the snake gone into the body / walls
        self.body.insert(0, move_coord)
        return move_coord

    def tunningWeights(self, snake, food):
        ate = False
        steps = []
        step_taken = 0

        # this will loop until win or lose have reached (the step_taken is to prevent stuck in a loop forever)
        while not (ate or snake.checkSnake() or step_taken >= Constants.SQUARE_AMOUNT*Constants.SQUARE_AMOUNT):
            step = EAEvaluation.accumulationEvaluation(snake, food, self.weights)
            move_coord = self.getCoordinate(step[0])

            self.body.insert(0, move_coord)
            steps.append(move_coord)
            ate = self.checkAte(food, self.body)
            step_taken += 1

        if ate:
            return True, steps

        return False, steps