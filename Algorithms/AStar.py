from Algorithms.Agent import Agent
from Game import squareAmount


class AStar():
    def __init__(self):
        self.cost_g = 0
        self.cost_h = 0
        self.face_direction = 0
        self.potential_steps = []

    def move(self,position,food):
        #cost_h is the cheapest path from the head to the food
        if (position[0][0] + 1 < squareAmount):


        self.cost_h =
        self.cost_g += 1

        return position