import copy

from Algorithms.AStar import AStar
from Algorithms.AlmightyMove import AlmightyMove
from Algorithms.BestFirstSearchPlus import BestFirstSearchPlus
from Algorithms.RandomSearchPlus import RandomSearchPlus
from Food import Food
from SnakeLogic import SnakeLogic

from UpdateValues import updateOtherFood, updateOtherAlgo, resetDefeat, clearSteps


def updateSnake(snake, snake_food):
    ate = False

    if (snake.body[0][0] == snake_food.foodX) and (snake.body[0][1] == snake_food.foodY):
        snake.checkSnake()
        ate = True

    return ate


class AccumulationAlgo(SnakeLogic):
    def __init__(self, name="algo"):
        super().__init__(name)

        self.a_star_static = AStar("static")
        self.a_star_dynamic = AStar("dynamic")
        self.random = RandomSearchPlus()
        self.BFS = BestFirstSearchPlus()
        self.almighty = AlmightyMove()

        self.body = copy.copy(self.a_star_static.body)

        updateOtherAlgo(self.a_star_static, self.BFS, self.random, self.almighty, self.a_star_dynamic)

        self.a_star_static_food = Food(self.a_star_static.body)
        self.BFS_food = Food(self.BFS.body)
        self.a_star_dynamic_food = Food(self.a_star_dynamic.body)
        self.random_food = Food(self.random.body)
        self.almighty_food = Food(self.almighty.body)

        updateOtherFood(self.a_star_static_food, self.almighty_food, self.BFS_food, self.random_food,
                        self.a_star_dynamic_food)

        self.a_star_static_moves = []
        self.a_star_dynamic_moves = []
        self.BFS_moves = []
        self.random_moves = []
        self.almighty_moves = []

        self.almighty_defeat = False
        self.BFS_defeat = False
        self.random_defeat = False
        self.a_star_static_defeat = False
        self.a_star_dynamic_defeat = False

        self.completed = None
        self.found_solution = False

        self.defeated = False

    def move(self, food):
        if not self.found_solution:
            updateOtherFood(food, self.almighty_food, self.random_food, self.a_star_dynamic_food,
                            self.a_star_static_food)
            self.BFS_food.foodX = food.foodX
            self.BFS_food.foodY = food.foodY

        if self.found_solution:
            self.body.insert(0, self.completed.pop(0))

            if self.checkAte(food, self.body):
                self.found_solution = False

            elif not self.completed:
                self.found_solution = False
                self.body = copy.copy(self.a_star_static.body)
                self.defeated = True

        else:
            while True:
                if not self.a_star_static_defeat and not self.found_solution:
                    if not self.a_star_static.path:
                        self.a_star_static.getPath(self.a_star_static_food)

                    if self.a_star_static.path:
                        self.a_star_static_moves.append(self.a_star_static.move(self.a_star_static_food))

                    if updateSnake(self.a_star_static, self.a_star_static_food):
                        self.found_solution = True
                        updateOtherAlgo(self.a_star_static, self.BFS, self.random, self.almighty, self.a_star_dynamic)

                        self.completed = self.a_star_static_moves

                        self.a_star_dynamic_moves, self.BFS_moves, self.almighty_moves, self.random_moves, self.a_star_static_moves = clearSteps()

                        self.almighty_defeat, self.BFS_defeat, self.random_defeat, self.a_star_static_defeat, self.a_star_dynamic_defeat = resetDefeat()
                        self.a_star_static.path = []
                        self.a_star_dynamic.path = []
                        break

                if not self.BFS_defeat and not self.found_solution:
                    move = self.BFS.move(self.BFS_food)
                    if move:
                        self.BFS_moves.append(move)

                    if updateSnake(self.BFS, self.BFS_food):
                        self.found_solution = True
                        updateOtherAlgo(self.a_star_static, self.BFS, self.random, self.almighty, self.a_star_dynamic)

                        self.completed = self.BFS_moves

                        self.a_star_dynamic_moves, self.BFS_moves, self.almighty_moves, self.random_moves, self.a_star_static_moves = clearSteps()

                        self.almighty_defeat, self.BFS_defeat, self.random_defeat, self.a_star_static_defeat, self.a_star_dynamic_defeat = resetDefeat()
                        self.a_star_static.path = []
                        self.a_star_dynamic.path = []
                        break

                if not self.random and not self.found_solution:
                    move = self.random.move(self.random_food)

                    if move:
                        self.random_moves.append(move)

                    if updateSnake(self.random, self.random_food):
                        self.found_solution = True
                        updateOtherAlgo(self.a_star_static, self.BFS, self.random, self.almighty, self.a_star_dynamic)

                        self.completed = self.random_moves

                        self.a_star_dynamic_moves, self.BFS_moves, self.almighty_moves, self.random_moves, self.a_star_static_moves = clearSteps()

                        self.almighty_defeat, self.BFS_defeat, self.random_defeat, self.a_star_static_defeat, self.a_star_dynamic_defeat = resetDefeat()
                        self.a_star_static.path = []
                        self.a_star_dynamic.path = []
                        break

                if not self.almighty_defeat and not self.found_solution:
                    move = self.almighty.move(self.almighty_food)

                    if move:
                        self.almighty_moves.append(move)

                    if updateSnake(self.almighty, self.almighty_food):
                        self.found_solution = True
                        updateOtherAlgo(self.a_star_static, self.BFS, self.random, self.almighty, self.a_star_dynamic)

                        self.completed = self.almighty_moves

                        self.a_star_dynamic_moves, self.BFS_moves, self.almighty_moves, self.random_moves, self.a_star_static_moves = clearSteps()

                        self.almighty_defeat, self.BFS_defeat, self.random_defeat, self.a_star_static_defeat, self.a_star_dynamic_defeat = resetDefeat()
                        self.a_star_static.path = []
                        self.a_star_dynamic.path = []
                        break

                if not self.a_star_dynamic_defeat and not self.found_solution:
                    self.a_star_dynamic.getPath(self.a_star_dynamic_food)

                    if self.a_star_dynamic.path:
                        self.a_star_dynamic_moves.append(self.a_star_dynamic.move(self.a_star_dynamic_food))

                    if updateSnake(self.a_star_dynamic, self.a_star_dynamic_food):
                        self.found_solution = True
                        updateOtherAlgo(self.a_star_static, self.BFS, self.random, self.almighty, self.a_star_dynamic)

                        self.completed = self.a_star_dynamic_moves

                        self.a_star_dynamic_moves, self.BFS_moves, self.almighty_moves, self.random_moves, self.a_star_static_moves = clearSteps()

                        self.almighty_defeat, self.BFS_defeat, self.random_defeat, self.a_star_static_defeat, self.a_star_dynamic_defeat = resetDefeat()

                        self.a_star_static.path = []
                        self.a_star_dynamic.path = []
                        break

                if self.almighty_defeat and self.BFS_defeat and self.random_defeat and self.a_star_static_defeat and self.a_star_dynamic_defeat:
                    self.found_solution = True
                    updateOtherAlgo(self.a_star_static, self.BFS, self.random, self.almighty, self.a_star_dynamic)

                    algo_dict = {"a_star_static_moves": len(self.a_star_static_moves),
                                 "a_star_dynamic_moves": len(self.a_star_dynamic_moves),
                                 "BFS_moves": len(self.BFS_moves),
                                 "random_moves": len(self.random_moves),
                                 "almighty_moves": len(self.almighty_moves)}

                    algo_moves_dict = {"a_star_static_moves": self.a_star_static_moves,
                                       "a_star_dynamic_moves": self.a_star_dynamic_moves,
                                       "BFS_moves": self.BFS_moves,
                                       "random_moves": self.random_moves,
                                       "almighty_moves": self.almighty_moves}

                    self.completed = algo_moves_dict[max(algo_dict, key=algo_dict.get)]

                    self.a_star_static_food.randomFood(self.a_star_static.body)

                    updateOtherFood(self.a_star_static_food, self.BFS_food, self.random_food,
                                    self.almighty_food, self.a_star_dynamic_food)

                    self.a_star_dynamic_moves, self.BFS_moves, self.almighty_moves, self.random_moves, self.a_star_static_moves = clearSteps()

                    self.almighty_defeat, self.BFS_defeat, self.random_defeat, self.a_star_static_defeat, self.a_star_dynamic_defeat = resetDefeat()
                    break

            if self.completed:
                self.body.insert(0, self.completed.pop(0))
                if self.checkAte(food, self.body):
                    self.found_solution = False
            else:
                self.found_solution = False
                self.body = copy.copy(self.a_star_static.body)
                self.defeated = True
