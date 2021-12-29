import pygame as pg
from Player import Player
from Block import *
from Utilites import *


BLS = 50


pg.init()
pg.mouse.set_visible(False)
run, tobreak = True, False
screen = pg.display.set_mode(size := (1000, 600))
pg.display.set_caption('WOAAAAH WHAT IS THIS MONSTER!!!')
layers = [pg.Surface(size) for _ in range(st.maxheight)]
objs = [pg.sprite.Group() for _ in range(st.maxheight)]
dists = [[0] * st.rays for _ in range(st.maxheight)]
plrs = pg.sprite.Group()
plr = Player(BLS, size, plrs)
fov = radians(st.fov)
step = fov / st.rays
angle = 0
clock = pg.time.Clock()
pressed = [False] * 4
keys = [pg.K_w, pg.K_s, pg.K_a, pg.K_d]
block_image = pg.Surface((BLS, BLS))
pg.draw.rect(block_image, (255, 0, 255), (0, 0, BLS, BLS))
Block(objs[1], block_image, 2, 4, 1)
while run:
    tick = clock.tick()
    screen.fill((0, 0, 0))
    pc = plr.get_centre()
    for i in range(st.maxheight):
        layers[i].fill((0, 0, 0))
        plrs.draw(layers[i])
        objs[i].draw(layers[i])
        for rayn in range(st.rays):
            sn = optsin(angle - fov + rayn * step)
            cs = optcos(angle - fov + rayn * step)
            for ray in range(st.raylen):
                pg.draw.line(layers[i], (255, 255, 255), pc, (pc[0] + ray * cs, pc[1] + ray * sn))
                tobreak = False
                for r in rects[i]:
                    if r[0] <= pc[0] + ray * cs <= r[0] + BLS and r[1] <= pc[1] + ray * sn <= r[1] + BLS:
                        tobreak = True
                        break
                if tobreak:
                    dists[i][rayn] = round(ray * math.sqrt(cs ** 2 + sn ** 2))
                    break
            if not tobreak:
                dists[i][rayn] = 0
    screen.blit(layers[1], (0, 0))
    for i in range(4):
        if pressed[i]:
            if i < 2:
                plr.update(0, tick * 2 * (2 * i - 1))
            else:
                plr.update(tick * 2 * (2 * i - 5), 0)
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
            print(dists)
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