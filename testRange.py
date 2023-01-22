from Constants import SQUARE_AMOUNT
from Directions import Directions
square = 6
template_path_0 = []
for x in range(square):
    for y in range(square):
        # odd
        if x % 2:
            template_path_0.append([[x, y], Directions.DOWN])
        # even
        else:
            template_path_0.append([[x, y], Directions.UP])


# this part changes the direction
for i in template_path_0:
    if i[0][1] == square - 1 and not i[0] == [0, square - 1]:
        i[1] = Directions.LEFT
    elif i[0][1] == 0 and not i[0][0] % 2:
        i[1] = Directions.RIGHT
    elif i[0][0] % 2 and i[0][1] == square - 2 and not i[0] == [square - 1, square - 2]:
        i[1] = Directions.RIGHT

print(template_path_0)
for index, i in enumerate(template_path_0):
    print(index)
    if i[0] == [0,1]:
        print(i)
        break

square = 5
template_path_0 = []
for y in range(square):
    for x in range(square - 1):
        if x % 2:
            template_path_0.append([[x, y], Directions.DOWN])
        else:
            template_path_0.append([[x, y], Directions.UP])

for i in template_path_0.copy():
    if i[0] == [0, square]:
        i[1] = Directions.UP
    elif i[0] == [0, 0]:
        i[1] = Directions.RIGHT
    elif i[0][1] == square - 1 and not i[0] == [0, 4]:
        i[1] = Directions.LEFT
    elif i[0][0] % 2 and i[0][1] == square - 2 and not i[0] == [3,3]:
        i[1] = Directions.RIGHT
    elif not i[0][0] % 2 and i[0][1] == 1 and not i[0] == [0, 1]:
        i[1] = Directions.RIGHT
    elif i[0][0] in range(2, square - 1) and i[0][1] == 0:
        template_path_0.remove(i)

print(template_path_0)
print(len(template_path_0))

template_path_1 = []
for y in range(square):
    for x in range(1, square):
        if x % 2:
            template_path_1.append([[x, y], Directions.DOWN])
        else:
            template_path_1.append([[x, y], Directions.UP])

for i in template_path_1.copy():
    if i[0] == [square - 2, square - 1]:
        i[1] = Directions.RIGHT
    if i[0] == [1, 0]:
        i[1] = Directions.DOWN
    elif i[0][1] == 0:
        i[1] = Directions.LEFT
    elif i[0][1] == 1 and i[0][0] < square - 1 and not i[0][0] % 2:
        i[1] = Directions.RIGHT
    elif i[0][1] == square - 2 and i[0][0] % 2 and not i[0] == [square-2, square-2]:
        i[1] = Directions.RIGHT
    elif i[0][0] in range(1, square - 2) and i[0][1] == square - 1:
        template_path_1.remove(i)

print(template_path_1)
print(len(template_path_1))


