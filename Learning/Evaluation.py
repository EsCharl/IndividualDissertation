import Constants

# this is the weight for the training (might have different implementation down the line)
training_weight = [4, 2, 4, 2, 4, 2]


# this function is used for evaluation of the move.
# If the move made can reach the food then it will be considered (score > 0 else score = 0).
# from "Snake game AI: Movement rating functions and evolutionary algorithm-based optimization"
def foodMoveEvaluation(space_value, space_list, food, possible_head):
    # the distance is the distance if the snake makes the move to there
    # print(space_value, space_list, [food.foodX, food.foodY], possible_head)
    if [food.foodX, food.foodY] in space_list:
        # the plus 1 is to ensure not divided by 0 (if the possible head is the food)
        distance = abs(possible_head[0] - food.foodX) + abs(possible_head[1] - food.foodY) + 1
        score = space_value / distance
    else:
        score = 0
    return score


# this will generate and select the best evaluation based on the available move (Left, Forward, Right)
def accumulationEvaluation(snake, food):
    final_scores = []

    # the move_list is a list with 3 array inside. (Left, Forward, Right moves)
    move_list = snake.generateSpaceListBasedOnAvailableMoves(True)
    space_score_list = snake.generateSpaceListBasedOnAvailableMoves(False)
    # print(space_score_list)

    for index, move in enumerate(move_list):
        final_score_list = []
        extract_space_list = []

        for i in space_score_list[index][0]:
            extract_space_list.append(i[1])

        # this print is used to get the coordinates that it could go.
        # print(move)

        if move[0]:
            # this is to get the smoothness value
            maximum = 0
            for i in move[0]:
                if i[0] > maximum:
                    maximum = i[0]

            # first will be smoothness
            # second will be space
            # third will be foodMoveEval
            final_score_list.append(maximum)
            final_score_list.append(len(space_score_list[index]))
            final_score_list.append(
                foodMoveEvaluation(len(space_score_list[index]), extract_space_list, food, move[0][0][1]))

        else:
            final_score_list.append(0)

        # this section is used to multiply and finalise the score for each direction.
        sum = 0
        for index, score in enumerate(final_score_list):
            sum += score * (training_weight[(index + 1) * 2 - 2] + (
                    training_weight[(index + 1) * 2 - 1] * len(snake.body) / (
                    Constants.SQUARE_AMOUNT * Constants.SQUARE_AMOUNT)))

        final_scores.append(sum)

    final_score = max(final_scores)
    return final_scores.index(final_score), final_score
