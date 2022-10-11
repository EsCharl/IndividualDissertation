from Algorithms.Agent import Agent
from Game import squareAmount


class BestFirstSearch():
    def __init__(self):
        self.face_direction = 0

    def move(self, position, food):
        fixed_step = None
        potential_steps = []
        # cost_h is the cheapest path from the head to the food

        # this ensures that the snake could go to all position
        # than the borders
        if (position[0][0] + 1 < squareAmount):
            potential_steps.append(position[0])
        if (position[0][0] - 1 >= 0):
            potential_steps.append(position[0])
        if (position[0][1] + 1 < squareAmount):
            potential_steps.append(position[0])
        if (position[0][1] - 1 >= 0):
            potential_steps.append(position[0])

        # this part is used to sort out the position where it doesn't reach the snake body
        steps = []
        for u in potential_steps:
            flag = 1
            for d in position:
                if d == u:
                    flag = 0
            if flag:
                steps.append(u)

        # this part gets the lowest cost which is able to get to the food
        lowest_cost_h = 999999
        for x in steps:
            manhattan_distance = (abs(food[0] - x[0]) + abs(food[1] - x[1]))
            if manhattan_distance < lowest_cost_h:
                lowest_cost_h = manhattan_distance
                fixed_step = x

        # this part is used return if the snake have successfully
        # found a valid place
        if fixed_step != None:
            position.append(fixed_step)
            return False, position
        else:
            return True, position
