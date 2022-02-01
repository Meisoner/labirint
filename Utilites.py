import math
import pygame as pg
from Settings import st


# Ошибка установки небезопасных параметров лабиринта.
class SafeGenerationError(Exception):
    pass


PI = math.pi
sins = dict()
coses = dict()


def radians(x):
    return x * PI / 180


# Оптимизированная функция синуса.
def optsin(x):
    rx = int(x * 10 ** 5) / 10 ** 5
    if rx in sins.keys():
        return sins[rx]
    sins[rx] = math.sin(x)
    return sins[rx]


# Оптимизированная функция косинуса.
def optcos(x):
    rx = int(x * 10 ** 5) / 10 ** 5
    if rx in coses.keys():
        return coses[rx]
    coses[rx] = math.cos(x)
    return coses[rx]


# Функция для рисования блоков.
def draw(screen, size, height, ray, texture, yangle):
    x = ray * (size[0] // st.rays)
    y = size[1] // 2 + int(height / 2) + int((yangle - PI) * 300)
    screen.blit(texture, (x, size[1] - y))


def draw_enemy(screen, size, height, colour, ray):
    col = (colour, 0, 0)
    x = ray * (size[0] // st.rays), (size[0] // st.rays)
    y = size[1] // 2 + int(height / 2)
    for i in range(2):
        y1 = y + (height - 1) * i
        pg.draw.rect(screen, col, (x[0], size[1] - y1, x[1], height))


# Функция для рисования пола.
def draw_floor(screen, size, yangle):
    pg.draw.rect(screen, (70, 40, 20), (0, size[1] - 300 - (yangle - PI) * 300, size[0], 300 + (yangle - PI) * 300), 0)