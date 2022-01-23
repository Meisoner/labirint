from random import randrange as rr


def optimals(x, y, dists):
    res = []
    for i in range(len(dists)):
        if dists[i] >= 7:
            res += [[i, rr(3, 7)]]
    return res


def filtr(startpos, lab):
    lcopy = []
    for i in lab:
        lcopy += [[]]
        for j in i:
            lcopy[-1] += [j]
    for x in range(len(lab) - 1):
        for y in range(len(lab) - 1):
            kvo = 0
            for t1 in range(3):
                for t2 in range(3):
                    if lab[x + t1 - 1][y + t2 - 1] == 1:
                        kvo += 1
            if kvo == 9:
                lcopy[x][y] = 0
    lcopy[0] = [1] * len(lcopy[0])
    for i in range(len(lcopy)):
        lcopy[i][0] = 1
    lcopy[startpos[0]][startpos[1]] = 0
    return lcopy


def prototype(size, startpos):
    res = [[1] * size for _ in range(size)]
    x, y = startpos
    if x:
        napr = 0
    elif y:
        napr = 1
    else:
        return
    while True:
        res[x][y] = 0
        if napr == 1:
            x += 1
        elif napr == 2:
            x -= 1
        elif napr == 0:
            y += 1
        if size in (x, y):
            break
        if not rr(3):
            napr = 1 - int(bool(napr))
            if napr and not rr(4):
                napr += 1
    for i in range(200):
        res[rr(size - 2)][rr(size - 2)] = 0
#    goal = [x, y, 1, rr(1, 4)]
#    k = 1
#    while goal:
#        x, y = goal[0], goal[1]
#        for i in range(goal[3]):
#            x += int(goal[2] < 2) * (2 * goal[2] - 1)
#            y += int(goal[2] > 1) * (2 * goal[2] - 5)
#            res[y][x] = 0
#        if k <= 50:
#            dists = [x, size - x - 1, y, size - y - 1]
#            for j in optimals(x, y, dists):
#                goal += [x, y, j[0], j[1]]
#            k += 1
#        goal = goal[4:]
    return filtr(startpos, res)


def labirint(size, startpos):
    res = prototype(size, startpos)
    while any(res[-2][1:-1]):
        res = prototype(size, startpos)
    for i in res:
        for j in i:
            print(j, end='')
        print()
    return res


labirint(100, (0, 5))