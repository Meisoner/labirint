import math


PI = math.pi
sins = dict()
coses = dict()


def radians(x):
    return x * PI / 180


def optsin(x):
    rx = int(x * 10 ** 5) / 10 ** 5
    if rx in sins.keys():
        return sins[rx]
    sins[rx] = math.sin(x)
    return sins[rx]


def optcos(x):
    rx = int(x * 10 ** 5) / 10 ** 5
    if rx in coses.keys():
        return coses[rx]
    coses[rx] = math.cos(x)
    return coses[rx]