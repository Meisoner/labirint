import pygame as pg
from Settings import st


BLS = st.BLS


class Player(pg.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pg.Surface((BLS, BLS))
        pg.draw.rect(self.image, (100, 100, 100), (0, 0, 20, 20))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.dx = self.dy = 0
        self.hp = 100

    def get_centre(self):
        return (self.rect.x + self.rect.size[0] // 2, self.rect.y + self.rect.size[1] // 2)

    def update(self, x, y, total1, total2, total3):
        self.dx += x
        self.dy += y
        if not (-1 < self.dx < 1):
            self.rect.x += int(self.dx)
            self.dx -= int(self.dx)
        if not (-1 < self.dy < 1):
            self.rect.y += int(self.dy)
            self.dy -= int(self.dy)
        if pg.sprite.spritecollideany(self, total1):
            self.dx -= x
            self.dy -= y
        elif pg.sprite.spritecollideany(self, total2):
            self.dx -= x
            self.dy -= y
        elif pg.sprite.spritecollideany(self, total3):
            self.dx -= x
            self.dy -= y
            self.hp -= 2
        if self.hp > 0:
            return True
        else:
            return False

