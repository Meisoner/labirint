from Settings import st
import pygame as pg


BLS = st.BLS


# Основной класс для работы с текстурами.
class Texture:
    def __init__(self, img, quality, text=''):
        self.img = pg.image.load(img).convert()
        self.img = pg.transform.scale(self.img, (quality, quality))
        if text:
            font = pg.font.Font(None, 250)
            y = 0
            for line in text.split('\n'):
                rendline = font.render(line, True, (0, 0, 0))
                y += rendline.get_rect().height
                self.img.blit(rendline, (0, y))
        self.quality = quality
        self.raywidth = quality // st.BLS

    def get(self, offs, height):
        offset = int(offs) % BLS
        return pg.transform.scale(self.img.subsurface(offset * self.raywidth, 0, self.raywidth, self.quality),
                                  (2, int(height)))
