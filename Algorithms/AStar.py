from Constants import SQUARE_AMOUNT
from SnakeLogic import SnakeLogic


class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class AStar(SnakeLogic):
    def __init__(self):
        self.face_direction = 0
        self.reset()
        self.defeated = False

    def reset(self):
        super(AStar, self).reset()
        self.path = []

    def search_new_node(self, parent, food, open_list, closed_list):
        lists = []

        adjacent = [[parent.position[0] + 1, parent.position[1]], [parent.position[0] - 1, parent.position[1]],
                    [parent.position[0], parent.position[1] + 1], [parent.position[0], parent.position[1] - 1]]
        for x in adjacent:
            found = False
            for closed in closed_list:
                if closed.position == x:
                    found = True
            if not (x in self.body or x[0] < 0 or x[0] > SQUARE_AMOUNT - 1 or x[1] < 0 or x[
                1] > SQUARE_AMOUNT - 1) and not found:
                for N in open_list:
                    if N.position == x:
                        g = parent.g + 1
                        h = abs(x[0] - food.foodX) + abs(x[1] - food.foodY)
                        f = g + h
                        found = True
                        if f < N.f:
                            N.f = f
                            N.parent = parent
                        continue
                if not found:
                    node = Node(parent, x)
                    node.g = parent.g + 1
                    node.h = abs(x[0] - food.foodX) + abs(x[1] - food.foodY)
                    node.f = node.g + node.h
                    lists.append(node)

        return lists

    def getPath(self, food):
        path = []
        start_node = Node(None, self.body[0])
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, [food.foodX, food.foodY])
        end_node.g = end_node.h = end_node.f = 0

        open_list = []
        closed_list = []

        open_list.append(start_node)

        while len(open_list):
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                # get the lowest f cost
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            open_list.pop(current_index)
            closed_list.append(current_node)

            # if the end node is found
            if current_node.position == end_node.position:
                found = True
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                self.path = path[::-1]
                self.path.pop(0)
                open_list = []
            else:
                open_list.extend(self.search_new_node(current_node, food, open_list, closed_list))

        if not path:
            neighbours = self.generateAllPotentialSteps()
            lowest_cost_h = 999999
            fixed_step = None

            for step in neighbours:
                if step not in self.body:
                    manhattan_distance = (abs(food.foodX - step[0]) + abs(food.foodY - step[1]))
                    if manhattan_distance < lowest_cost_h:
                        lowest_cost_h = manhattan_distance
                        fixed_step = step

            if fixed_step:
                self.path.append(fixed_step)


        if not self.path:
            self.reset()
            self.defeated = True
            # except IndexError:
            #     # print(checked)
            #     if not checked == []:
            #         self.path.append(checked[0][1])
            #         # print("t", self.path)
            #     else:
            #         self.reset()
            #         # self.getPath(food)
            #         self.defeated = True
            #     break

    def move(self, food):
        self.body.insert(0, self.path.pop(0))
        self.checkAte(food, self.body)
