import pygame as pg
from Settings import st


BLS = st.BLS


class Player(pg.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pg.Surface((20, 20))
        pg.draw.rect(self.image, (100, 100, 100), (0, 0, 20, 20))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 125, -30
        self.dx = self.dy = 0

    def get_centre(self):
        return (self.rect.x + self.rect.size[0] // 2, self.rect.y + self.rect.size[1] // 2)

    def update(self, x, y, objs, deb):
        backup = self.rect.x, self.rect.y, self.dx, self.dy
        self.dx += x
        self.dy += y
        if not (-1 < self.dx < 1):
            self.rect.x += int(self.dx)
            self.dx -= int(self.dx)
        if not (-1 < self.dy < 1):
            self.rect.y += int(self.dy)
            self.dy -= int(self.dy)
        if not deb:
            if pg.sprite.spritecollideany(self, objs):
                backup2 = self.rect.x, self.dx
                self.rect.x, self.dx = backup[0], backup[2]
                if pg.sprite.spritecollideany(self, objs):
                    self.rect.x, self.dx = backup2
                    self.rect.y, self.dy = backup[1], backup[3]
                    if pg.sprite.spritecollideany(self, objs):
                        self.rect.x, self.rect.y, self.dx, self.dy = backup

    def get_block(self):
        return self.rect.x // BLS, self.rect.y // BLS