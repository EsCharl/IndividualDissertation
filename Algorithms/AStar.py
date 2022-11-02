from queue import PriorityQueue

from Constants import SQUARE_AMOUNT
from SnakeLogic import SnakeLogic


class AStar(SnakeLogic):
    def __init__(self):
        self.face_direction = 0
        self.reset()

    def reset(self):
        super(AStar, self).reset()
        self.path = []

    def search(self, body, check, food):
        neighbours = []

        neighbours.append([check[0] + 1, check[1]])
        neighbours.append([check[0] - 1, check[1]])
        neighbours.append([check[0], check[1] + 1])
        neighbours.append([check[0], check[1] - 1])

        unfulfilled_filtering = []

        for x in neighbours:
            # this part filters the location where the snake can't go
            if not (x in body or x[0] < 0 or x[0] > SQUARE_AMOUNT - 1 or x[1] < 0 or x[1] > SQUARE_AMOUNT - 1):
                unfulfilled_filtering.append((abs(x[0] - food.foodX) + abs(x[1] - food.foodY), x))

        return unfulfilled_filtering

    # this part needs further testing. but based on current checking it should work.
    def findPath(self, checked):
        path = []
        index = 0
        for i in checked:
            if path == []:
                cost = i[0]
                path.append(i[1])
            else:
                if i[0] < cost and (abs(path[index][0] - i[1][0]) + abs(path[index][1] - i[1][1]) == 1):
                    path.append(i[1])
                    cost = i[0]
                    index += 1
        return path

    def getPath(self, food):
        found_food = False
        checked = []

        soft_checked = self.search(self.body, self.body[0], food)
        soft_checked.sort()

        for x in soft_checked:
            if x[1] in [food.foodX, food.foodY]:
                found_food = True

        index = 0
        # this is just like greedy search with extra steps (need further changing)
        # if can't find the path the algo will move like the best first search (need checking if work)
        while not found_food:
            try:
                # this part is used to move the index so it doesn't loop when there is no new addition of location
                if soft_checked[index] in checked:
                    index += 1
                else:
                    checked.append(soft_checked[index])
                    index = 0
                    unfiltered_completely = self.search(self.body, soft_checked[index][1], food)
                    for x in unfiltered_completely:
                        if x not in soft_checked:
                            soft_checked.append(x)
                            if x[1] == [food.foodX, food.foodY]:
                                checked.append(x)
                                found_food = True
                                self.path = self.findPath(checked)
                                break
                soft_checked.sort()
            except:
                if not checked == []:
                    self.path.append(checked[0][1])
                else:
                    self.reset()
                    self.getPath(food)
                break

    def move(self):
        self.body.insert(0,self.path.pop(0))
        self.checkAte()