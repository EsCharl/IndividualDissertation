from Algorithms.AStar import AStar
from Algorithms.AlmightyMove import AlmightyMove
from Algorithms.BestFirstSearchPlus import BestFirstSearchPlus
from Algorithms.RandomSearchPlus import RandomSearchPlus
from Food import Food

from UpdateValues import updateOtherFood, updateOtherAlgo, resetDefeat, clearSteps

class AccumulationAlgo:
    def __init__(self):
        self.a_star_static = AStar("static")
        self.a_star_dynamic = AStar("dynamic")
        self.random = RandomSearchPlus()
        self.BFS = BestFirstSearchPlus()
        self.almighty = AlmightyMove()

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
