import math
import pygame as pg
from Settings import st


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


def draw(screen, size, height, colour, ray, layers, t):
    if t == 1:
        col = (colour, colour, colour)
        x = ray * (size[0] // st.rays), (size[0] // st.rays)
        y = size[1] // 2 + int(height / 2)
        for i in layers:
            y1 = y + (height - 1) * (i - 1)
            pg.draw.rect(screen, col, (x[0], size[1] - y1, x[1], height))
    else:
        col = (0, colour, 0)
        x = ray * (size[0] // st.rays), (size[0] // st.rays)
        y = size[1] // 2 + int(height / 2)
        for i in layers:
            y1 = y + (height - 1) * (i - 1)
            pg.draw.rect(screen, col, (x[0], size[1] - y1 / 1.5, x[1], height))