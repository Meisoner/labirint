from Settings import st
import pygame as pg


BLS = st.BLS


class Texture:
    def __init__(self, img, quality):
        self.img = pg.image.load(img).convert()
        self.img = pg.transform.scale(self.img, (quality, quality))
        self.quality = quality
        self.raywidth = quality // st.BLS

    def get(self, offs, height):
        offset = int(offs) % BLS
#        print(offset * self.raywidth, 0, self.raywidth, self.quality)
        return pg.transform.scale(self.img.subsurface(offset * self.raywidth, 0, self.raywidth, self.quality),
                                  (2, height))