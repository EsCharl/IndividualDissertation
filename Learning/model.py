from collections import namedtuple

import Constants
from SnakeLogic import SnakeLogic
import Evaluation

Point = namedtuple('Point', 'x y')
class Agent(SnakeLogic):

    def __init__(self, weights):
        self.score = 0
        self.reset()
        self.weights = weights

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

    def checkSnake(self):
        if self.body[0][0] < 0 or self.body[0][1] > Constants.SQUARE_AMOUNT - 1 or self.body[0][0] \
                > Constants.SQUARE_AMOUNT - 1 or self.body[0][1] < 0:
            return True

        for x in self.body[1:]:
            if self.body[0] == x:
                return True

        return False

    def move(self, snake, food):
        step = Evaluation.accumulationEvaluation(snake, food, self.weights)

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
            step = Evaluation.accumulationEvaluation(snake, food, self.weights)
            move_coord = self.getCoordinate(step[0])

            self.body.insert(0, move_coord)
            steps.append(move_coord)
            ate = self.checkAte(food, self.body)
            step_taken += 1

        if ate:
            return True, steps

        return False, steps

    # def get_name(self):
    #     return self.name
    #
    # def get_state(self, game):
    #     head = game.snake[0]
    #     point_l = Point(head.x - 20, head.y)
    #     point_r = Point(head.x + 20, head.y)
    #     point_u = Point(head.x, head.y - 20)
    #     point_d = Point(head.x, head.y + 20)
    #
    #     dir_l = game.direction == Directions.LEFT
    #     dir_r = game.direction == Directions.RIGHT
    #     dir_u = game.direction == Directions.UP
    #     dir_d = game.direction == Directions.DOWN
    #
    #     state = [
    #         # Danger straight
    #         (dir_r and game.is_collision(point_r)) or
    #         (dir_l and game.is_collision(point_l)) or
    #         (dir_u and game.is_collision(point_u)) or
    #         (dir_d and game.is_collision(point_d)),
    #
    #         # Danger right
    #         (dir_u and game.is_collision(point_r)) or
    #         (dir_d and game.is_collision(point_l)) or
    #         (dir_l and game.is_collision(point_u)) or
    #         (dir_r and game.is_collision(point_d)),
    #
    #         # Danger left
    #         (dir_d and game.is_collision(point_r)) or
    #         (dir_u and game.is_collision(point_l)) or
    #         (dir_r and game.is_collision(point_u)) or
    #         (dir_l and game.is_collision(point_d)),
    #
    #         # Move direction
    #         dir_l,
    #         dir_r,
    #         dir_u,
    #         dir_d,
    #
    #         # Food location
    #         game.food.x < game.head.x,  # food left
    #         game.food.x > game.head.x,  # food right
    #         game.food.y < game.head.y,  # food up
    #         game.food.y > game.head.y  # food down
    #     ]
    #
    #     return np.array(state, dtype=int)