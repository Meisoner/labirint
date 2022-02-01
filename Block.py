import pygame as pg
from Settings import st


BLS = st.BLS
rects = list()


# Класс для работы с блоками на двумерном поле.
class Block(pg.sprite.Sprite):
    def __init__(self, group, image, x, y):
        global rects
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * BLS, y * BLS
        rects += [(x * BLS, y * BLS)]