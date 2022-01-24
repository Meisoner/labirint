from random import randrange as rr


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
    try:
        res = [[1] * size for _ in range(size)]
        x, y = startpos
        if x:
            napr = 0
        elif y:
            napr = 1
        else:
            return
        rzv = []
        ln = 0
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
            ln += 1
            if not rr(3) and ln:
                napr = 1 - int(bool(napr))
                if napr and not rr(4):
                    napr += 1
                if napr:
                    rzv += [(x, y, 3 - napr)]
                ln = 0
        if y == size:
            endpos = x, y - 1
        else:
            return [[1, 1, 1] for _ in range(3)], (0, 0)
        for i in rzv:
            x, y = i[0], i[1]
            napr = i[2]
            if 7 < x < size - 7:
                for i in range(rr(2, 6)):
                    if napr == 1:
                        x += 1
                    else:
                        x -= 1
                    res[x][y] = 0
                res[x][y + 1] = 0
    except Exception:
        return [[1, 1, 1] for _ in range(3)], (0, 0)
    return filtr(startpos, res), endpos


def labirint(size, startpos):
    res = prototype(size, startpos)
    while any(res[0][-2][1:-1]):
        res = prototype(size, startpos)
    return res