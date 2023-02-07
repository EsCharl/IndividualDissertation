from Constants import SQUARE_AMOUNT
from SnakeLogic import SnakeLogic


class AStar(SnakeLogic):
    def __init__(self, name="A-Star"):
        super().__init__(name)
        self.face_direction = 0
        self.reset()
        self.defeated = False

    def reset(self):
        super(AStar, self).reset()
        self.path = []

    # gives all the available tiles that are neighbours of check
    def search(self, body, check, food):
        neighbours = [[check[0] + 1, check[1]], [check[0] - 1, check[1]], [check[0], check[1] + 1],
                      [check[0], check[1] - 1]]

        unfulfilled_filtering = []

        for x in neighbours:
            # this part filters the location where the snake can't go
            if not (x in body or x[0] < 0 or x[0] > SQUARE_AMOUNT - 1 or x[1] < 0 or x[1] > SQUARE_AMOUNT - 1):
                unfulfilled_filtering.append((abs(x[0] - food.foodX) + abs(x[1] - food.foodY), x))

        return unfulfilled_filtering

    def findPath(self, checked, food):

        while True:
            last_added_index = 0
            path = []
            index = 0
            for i in checked:
                if not path:
                    path.append(i[1])
                else:
                    if abs(path[index][0] - i[1][0]) + abs(path[index][1] - i[1][1]) == 1:
                        path.append(i[1])
                        index += 1
                        last_added_index = checked.index(i)
            if [food.foodX, food.foodY] in path:
                # print("FP",path)
                return path
            else:
                #     print(checked)
                #     print(path)
                #     print(checked.pop(last_added_index))
                checked.pop(last_added_index)

    def getPath(self, food):
        found_food = False
        checked = []

        soft_checked = self.search(self.body, self.body[0], food)
        soft_checked.sort()

        index = 0
        while not found_food:
            try:
                # this part is used to move the index, so it doesn't loop when there is no new addition of location
                if soft_checked[index] in checked:
                    index += 1
                else:
                    checked.append(soft_checked[index])
                    unfiltered_completely = self.search(self.body, soft_checked[index][1], food)
                    index = 0

                    for x in unfiltered_completely:
                        if x not in soft_checked:
                            soft_checked.append(x)

                            if x[1] == [food.foodX, food.foodY]:
                                checked.append(x)
                                found_food = True
                                # print("F", [food.foodX, food.foodY])
                                self.path = self.findPath(checked, food)
                                break

                soft_checked.sort()
            except IndexError:
                # print(checked)
                if not checked == []:
                    self.path.append(checked[0][1])
                    # print("t", self.path)
                else:
                    self.reset()
                    # self.getPath(food)
                    self.defeated = True
                break

    def move(self, food):
        step = self.path.pop(0)
        self.body.insert(0, step)
        self.checkAte(food, self.body)
        return step
