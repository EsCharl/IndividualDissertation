from copy import copy
from queue import PriorityQueue

from Constants import SQUARE_AMOUNT

# test = PriorityQueue()
#
# test.put((4.5, [1,6]))
# test.put((2.1, [1,5]))
# test.put((5, [1,3]))
# test.put((1.5, [1,2]))
# test.put((0, [1,1]))

# while not test.empty():
#     print(test.get())
def search(body, possible_steps, check):
    neighbours = []

    neighbours.append([check[0] + 1, check[1]])
    neighbours.append([check[0] - 1, check[1]])
    neighbours.append([check[0], check[1] + 1])
    neighbours.append([check[0], check[1] - 1])

    unfulfilled_filtering = []

    for x in neighbours:
        # this part filters the location where the snake can't go
        if not (x in body or x[0] < 0 or x[0] > SQUARE_AMOUNT - 1 or x[1] < 0 or x[1] > SQUARE_AMOUNT - 1):
            unfulfilled_filtering.append((abs(x[0] - foodX) + abs(x[1] - foodY), x))

    return unfulfilled_filtering

# this part needs further testing. but based on current checking it should work.
def findPath(checked):
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

if __name__ == '__main__':
    body = [[1, 2], [1, 3], [1, 4]]
    foodX = 6
    foodY = 6
    soft_checked = []
    found_food = False
    posible_steps = []
    index = 0
    checked = []
    path = []

    soft_checked = search(body, posible_steps, body[0])
    soft_checked.sort()

    for x in soft_checked:
        if x[1] in [foodX, foodY]:
            found_food = True

    lowest_cost = 999999
    index = 0
    # this is just like greedy search with extra steps (need further changing)
    # if can't find the path the algo will move like the best first search (need checking if work)
    while not found_food:
        try:
            # this part is used to move the index so it doesn't loop when there is no new addition of location
            if soft_checked[index] in checked:
                index += 1
            else:
                index = 0
                checked.append(soft_checked[index])
                unfiltered_completely = search(body, soft_checked, soft_checked[index][1])
                for x in unfiltered_completely:
                    if x not in soft_checked:
                        soft_checked.append(x)
                        if x[1] == [foodX, foodY]:
                            checked.append(x)
                            found_food = True
                            path = findPath(checked)
                            break

            soft_checked.sort()
        except:
            path.append([checked[0][1]])
            break

    print(path)
    # # this part is used to get all the available spaces
    # for x in range(SQUARE_AMOUNT):
    #     for y in range(SQUARE_AMOUNT):
    #         if not [x, y] in body:
    #             available_moves.append([x, y])
    #
    # # this part is used to get the distance between the available position to the food
    # # and also the distance between the head and the cost req to get to the position
    # # lastly put it all into a tuple
    # for move in available_moves:
    #     food_manhattan_distance = abs(move[0] - foodX) + abs(move[1] - foodY)
    #     manhattan_distance = abs(move[0] - body[0][0]) + abs(move[1] - body[0][1])
    #     possible_moves.append([food_manhattan_distance,move, manhattan_distance])
    #
    # possible_moves.sort()
    # from_snake = []
    # from_food = []
    #
    # # this part split the closest distance between the head of the snake to the location and the food to the location
    # for x in possible_moves:
    #     if x[0] > x[2]:
    #         from_snake.append(x)
    #     elif x[0] < x[2]:
    #         from_food.append(x)
    #     else:
    #         from_snake.append(x)
    #         from_food.append(x)
    #
    # first = True
    # path = []
    # for step in possible_moves:
    #     if first:
    #         first = False
    #         starting = step[1]
    #         path.append(step[1])
    #         costing = step[2] - 1
    #     else:
    #         if abs(starting[0] - step[1][0]) + abs(starting[1] - step[1][1]) == 1 and costing == step[2]:
    #             path.insert(0,step[1])
    #             print(step)
    #             starting = step[1]
    #             costing += 1
    #
    # print(path)
