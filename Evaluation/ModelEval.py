import copy

from Food import Food
from SnakeLogic import SnakeLogic
from Algorithms.Model import Model


def updateSnake(snake, snake_food):
    ate = False

    if (snake.body[0][0] == snake_food.foodX) and (snake.body[0][1] == snake_food.foodY):
        snake.checkSnake()
        ate = True

    return ate


class ModelEval(SnakeLogic):
    def __init__(self, weights, name="Generated Model"):
        super().__init__(name)

        self.model = Model(weights)
        self.model_food = Food(self.model.body)

        self.body = copy.copy(self.model.body)

        self.completed = []
        self.found_solution = False

        self.defeated = False

    def move(self, food):
        if not self.found_solution:
            self.model_food.foodX = food.foodX
            self.model_food.foodY = food.foodY

        if self.found_solution:
            if self.completed:
                self.body.insert(0, self.completed.pop(0))

            if self.checkAte(food, self.body):
                self.found_solution = False

            elif not self.completed:
                self.found_solution = False
                self.defeated = True
                self.body = copy.copy(self.model.body)

        else:
            while True:

                if not self.model.defeated and not self.found_solution:
                    move = self.model.move(self.model_food)

                    if move:
                        self.completed.append(move)

                    if updateSnake(self.model, self.model_food):
                        print(self.model.name)

                        self.found_solution = True
                        break

                if self.model.defeated:
                    print("none")
                    self.found_solution = True
                    self.model.defeated = False
                    break

            if self.completed:
                self.body.insert(0, self.completed.pop(0))
                if self.checkAte(food, self.body):
                    self.found_solution = False
            else:
                self.found_solution = False
                self.body = copy.copy(self.model.body)
                self.defeated = True
