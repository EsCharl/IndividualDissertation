from SnakeLogic import SnakeLogic


class BestFirstSearch(SnakeLogic):
    def __init__(self):
        self.reset()

    def move(self, food):
        fixed_step = None
        potential_steps = []
        # cost_h is the cheapest path from the head to the food

        potential_steps.append([self.body[0][0] + 1, self.body[0][1]])
        potential_steps.append([self.body[0][0] - 1, self.body[0][1]])
        potential_steps.append([self.body[0][0], self.body[0][1] + 1])
        potential_steps.append([self.body[0][0], self.body[0][1] - 1])

        # this part is used to sort out the position where it doesn't reach the snake body
        steps = []
        for u in potential_steps:
            steps.append(u)

        # this part gets the lowest cost which is able to get to the food
        lowest_cost_h = 999999
        for x in steps:
            manhattan_distance = (abs(food.foodX - x[0]) + abs(food.foodY - x[1]))
            if manhattan_distance < lowest_cost_h:
                lowest_cost_h = manhattan_distance
                fixed_step = x

        # this part is used return if the snake have successfully
        # found a valid place
        if fixed_step != None:
            self.body.insert(0, fixed_step)
            self.checkAte()
        else:
            self.reset()
        return self.body
