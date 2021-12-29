import pygame as pg
from Settings import Settings

st = Settings('settings.txt')
rects = [list() for _ in range(st.maxheight)]


class Block(pg.sprite.Sprite):
    def __init__(self, group, image, x, y, lnum):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * 50, y * 50
        rects[lnum] += [(x * 50, y * 50)]