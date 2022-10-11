if __name__ == '__main__':
    y = [[1,2],[1,1],[1,2],[1,3]]
    for i in y:
        i[0]+=1
        print(i)
    y.pop()
    y.insert(0,[1,9])

    x = [[2,1], [3,1]]
    test = [ u for u in x if u == y]

    add = []
    for u in x:
        flag = 1
        for d in y:
            if d == u:
                flag = 0
        if flag:
           add.append(u)

    food = [3,1]
    steps = [[1,2],[0,1],[1,0],[2,1]]

    lowest_cost_h = 999999
    for x in steps:
        manhattan_distance = (abs(food[0] - x[0]) + abs(food[1] - x[1]))
        if manhattan_distance < lowest_cost_h:
            lowest_cost_h = manhattan_distance
            fixed_step = x

    print(fixed_step)
