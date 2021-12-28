import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, blsize, size, group):
        super().__init__(group)
        self.image = pg.Surface(blsize)
        pg.draw.rect(self.image, (255, 255, 255), (0, 0, 50, 50))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = size[0] // 2 - self.rect.size[0] // 2, size[1] // 2 - self.rect.size[1] // 2