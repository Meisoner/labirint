import pygame as pg
from Player import Player
from Settings import Settings
import math


BLS = (50, 50)


pg.init()
run = True
screen = pg.display.set_mode(size := (1000, 600))
pg.display.set_caption('WOAAAAH WHAT IS THIS MONSTER!!!')
layers = [pg.Surface(size) for _ in range(10)]
plrs, obj = [pg.sprite.Group() for _ in range(2)]
plr = Player(BLS, size, plrs)
st = Settings('Settings.txt')
fov = (st.fov * math.pi) / 180
step = math.sqrt((math.cos(fov) - 1) ** 2 + math.sin(fov) ** 2) / st.rays
angle = (1, 0)
while run:
    screen.fill((0, 0, 0))
    pc = plr.get_centre()
    for i in layers:
        i.fill((0, 0, 0))
        plrs.draw(i)
        for rayn in range(st.rays):
            for ray in range(st.raylen):
                pg.draw.line(i, (255, 255, 255), pc, (int((angle[0] - step * rayn) * ray * BLS[0]),
                                                      int((angle[1] - step * rayn) * ray * BLS[1])))
    screen.blit(layers[1], (0, 0))
    pg.display.flip()
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run = False
