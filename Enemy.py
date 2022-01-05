import pygame as pg
import random


class Enemy(pg.sprite.Sprite):
    def __init__(self, blsize, group):
        super().__init__(group)
        self.image = pg.Surface((blsize, blsize))
        pg.draw.rect(self.image, (0, 255, 0), (0, 0, 30, 30))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = random.randint(0, 1000), random.randint(0, 600)
        self.dx = self.dy = 0

    def get_centre(self):
        return (self.rect.x + self.rect.size[0] // 2, self.rect.y + self.rect.size[1] // 2)

    def update(self):
        self.dx += random.randint(-10, 10)
        self.dy += random.randint(-10, 10)


    def new(self):
        self.rect.x, self.rect.y = random.randint(0, 1000), random.randint(0, 600)

