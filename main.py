import pygame as pg
from Player import Player
from Settings import Settings
import math


BLS = (50, 50)
PI = math.pi


def radians(x):
    return x * PI / 180


pg.init()
pg.mouse.set_visible(False)
run = True
st = Settings('settings.txt')
screen = pg.display.set_mode(size := (1000, 600))
pg.display.set_caption('WOAAAAH WHAT IS THIS MONSTER!!!')
layers = [pg.Surface(size) for _ in range(st.maxheight)]
objs = [pg.sprite.Group() for _ in range(st.maxheight)]
plrs = pg.sprite.Group()
plr = Player(BLS, size, plrs)
fov = radians(st.fov)
step = fov / st.rays
angle = 0
clock = pg.time.Clock()
pressed = [False] * 4
keys = [pg.K_w, pg.K_s, pg.K_a, pg.K_d]
while run:
    tick = clock.tick()
    screen.fill((0, 0, 0))
    pc = plr.get_centre()
    for i in layers:
        i.fill((0, 0, 0))
        plrs.draw(i)
        for rayn in range(st.rays):
            sn = math.sin(angle - fov + rayn * step)
            cs = math.cos(angle - fov + rayn * step)
            for ray in range(st.raylen):
                pg.draw.line(i, (255, 255, 255), pc, (pc[0] + ray * cs * 10, pc[1] + ray * sn * 10))
    screen.blit(layers[1], (0, 0))
    for i in range(4):
        if pressed[i]:
            if i < 2:
                plr.update(0, tick * (2 * i - 1) / 5)
            else:
                i -= 2
                plr.update(tick * (2 * i - 1) / 5, 0)
    pg.display.flip()
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run = False
        elif i.type == pg.KEYDOWN:
            if i.key == pg.K_ESCAPE:
                run = False
            else:
                for key in range(4):
                    if i.key == keys[key]:
                        pressed[key] = True
        elif i.type == pg.KEYUP:
            for key in range(4):
                if i.key == keys[key]:
                    pressed[key] = False
        elif i.type == pg.MOUSEMOTION:
            angle += radians(i.pos[0] - size[0] // 2)
            if angle >= 2 * PI:
                angle = 0
            elif angle < 0:
                angle = 2 * PI
            pg.mouse.set_pos(size[0] // 2, size[1] // 2)