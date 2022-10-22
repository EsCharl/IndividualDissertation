import Constants


def checkSnake(snake):
    if snake.body[0][0] < 0 or snake.body[0][1] > Constants.squareAmount - 1 or snake.body[0][
        0] > Constants.squareAmount - 1 or snake.body[0][1] < 0:
        snake.reset()
    for x in snake.body[1:]:
        if snake.body[0] == x:
            snake.reset()
