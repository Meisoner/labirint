from random import randrange as rr


def optimals(x, y, dists):
    res = []
    for i in range(len(dists)):
        if dists[i] >= 7:
            res += [[i, rr(3, 7)]]
    return res


def labirint(size, startpos):
    res = [[1] * size for _ in range(size)]
    x, y = startpos
    res[y][x] = 0
    goal = [x, y, 1, rr(1, 4)]
    k = 1
    exit = 0
    while goal:
        x, y = goal[0], goal[1]
        for i in range(goal[3]):
            x += int(goal[2] < 2) * (2 * goal[2] - 1)
            y += int(goal[2] > 1) * (2 * goal[2] - 5)
            res[y][x] = 0
        if k <= 50:
            dists = [x, size - x - 1, y, size - y - 1]
#            print(optimals(x, y, dists))
#            print(dists)
#            for i in res:
#                    for j in i:
#                        print(j, end='')
#                    print()
#            print()
            for j in optimals(x, y, dists):
                if rr(2) == 0:
#                    print([x, y, j])
                    goal += [x, y, j[0], j[1]]
            k += 1
        goal = goal[4:]
    return res