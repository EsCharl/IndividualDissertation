from SnakeLogic import SnakeLogic


class BestFirstSearchPlus(SnakeLogic):
    def __init__(self, name="Best First Search"):
        super().__init__(name)
        self.reset()
        self.defeated = False

    def move(self, food):
        fixed_step = None

        # this ensures that the snake could go to all position other than the borders
        potential_steps = self.generateAllPotentialSteps()

        # this part is used to sort out the position where it doesn't reach the snake body
        steps = []
        for u in potential_steps:
            flag = 1
            for d in self.body:
                if d == u:
                    flag = 0
            if flag:
                steps.append(u)

        # this part gets the lowest cost which is able to get to the food
        lowest_cost_h = 999999
        for step in steps:
            manhattan_distance = (abs(food.foodX - step[0]) + abs(food.foodY - step[1]))
            if manhattan_distance < lowest_cost_h:
                lowest_cost_h = manhattan_distance
                fixed_step = step

        # this part is used return if the snake have successfully
        # found a valid place
        if fixed_step != None:
            self.body.insert(0, fixed_step)
            self.checkAte(food, self.body)
            return fixed_step
        else:
            self.reset()
            self.defeated = True
        # return self.body
