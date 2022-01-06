import pygame as pg
import random
from Settings import st

enemys = [list() for _ in range(st.maxheight)]

class Enemy(pg.sprite.Sprite):
    def __init__(self, blsize, img, group, kol):
        super().__init__(group)
        self.image = pg.Surface((blsize, blsize))
        pg.draw.rect(self.image, (0, 255, 0), (10, 10, 15, 15))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = random.randint(0, 1000), random.randint(0, 600)
        self.dx = self.dy = 0
        self.hp = 20
        self.img = img
        self.kol = kol
        enemys[self.kol] += [(self.rect.x, self.rect.y)]

    def get_centre(self):
        return (self.rect.x + self.rect.size[0] // 2, self.rect.y + self.rect.size[1] // 2)

    def update(self, x, y, total1, total2):
        self.rect.x += x
        self.rect.y += y
        if not (-1 < self.dx < 1):
            self.rect.x += int(self.dx)
            self.dx -= int(self.dx)
        if not (-1 < self.dy < 1):
            self.rect.y += int(self.dy)
            self.dy -= int(self.dy)
        if pg.sprite.spritecollideany(self, total1):
            self.rect.x -= x
            self.rect.y -= y
        if pg.sprite.spritecollideany(self, total2):
            self.rect.x -= x
            self.rect.y -= y
        enemys[self.kol] += [(self.rect.x, self.rect.y)]


    def new_pos(self):
        self.rect.x, self.rect.y = random.randint(0, 1000), random.randint(0, 600)

    def attack(self, domage):
        self.hp -= domage
        return self.hp
