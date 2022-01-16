import pygame as pg
# import random
from Settings import st


ENS = 20
BLS = st.BLS
enemy_rects = list()
enemyset = set()

class Enemy(pg.sprite.Sprite):
    def __init__(self, group, x, y):
        global enemy_rects, enemyset
        super().__init__(group)
        self.image = pg.Surface((ENS, ENS))
        pg.draw.rect(self.image, (0, 255, 0), (x * ENS, y * ENS, ENS, ENS))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * ENS, y * ENS
        self.dx = self.dy = 0
        self.hp = 20
        enemy_rects += [(self.rect.x, self.rect.y)]
        enemyset.add((self.rect.x, self.rect.y))
        print(enemy_rects, enemyset)
        self.num = len(enemy_rects) - 1

    def get_coords(self):
        return (self.rect.x, self.rect.y)

    def update(self, x, y): # , total1, total2):
        global enemyset
        self.dx += x
        self.dy += y
        if not (-1 < self.dx < 1):
            self.rect.x += int(self.dx)
            self.dx -= int(self.dx)
        if not (-1 < self.dy < 1):
            self.rect.y += int(self.dy)
            self.dy -= int(self.dy)
#        if not (-1 < self.dx < 1):
#            self.rect.x += int(self.dx)
#            self.dx -= int(self.dx)
#        if not (-1 < self.dy < 1):
#            self.rect.y += int(self.dy)
#            self.dy -= int(self.dy)
#        if pg.sprite.spritecollideany(self, total1):
#            self.rect.x -= x
#            self.rect.y -= y
#        if pg.sprite.spritecollideany(self, total2):
#            self.rect.x -= x
#            self.rect.y -= y
        enemy_rects[self.num] = (self.rect.x, self.rect.y)


#    def new_pos(self):
#        self.rect.x, self.rect.y = random.randint(0, 1000), random.randint(0, 600)
#        enemy_rects[self.num] = [(self.rect.x, self.rect.y)]

    def attack(self, damage):
        self.hp -= damage
        return self.hp

    def terminate(self):
        global enemyset
        enemy_rects[self.num] = ()