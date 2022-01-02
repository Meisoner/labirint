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
keys = [pg.K_w, pg.K_a, pg.K_s, pg.K_d]
block_image = pg.Surface((BLS, BLS))
pg.draw.rect(block_image, (255, 0, 255), (0, 0, BLS, BLS))
for i in range(2):
    Block(objs[1], block_image, 2, 4 + i, 1)
xdist, ydist = 0, 0
k = st.rays * BLS / (2 * math.tan(st.fov))
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
            if not sn:
                sn = 10 ** -5
            cs = optcos(angle - fov + rayn * step)
            if not cs:
                cs = 10 ** -5
            tg = sn / cs
            pc2 = [(i // BLS) * BLS for i in pc]
            sgn = [round(cs / abs(cs)), round(sn / abs(sn))]
            pc2[0] += BLS * ((sgn[0] + 1) // 2)
            pc2[1] += BLS * ((sgn[1] + 1) // 2)
            for _ in range(size[0] // BLS):
                y = pc[1] + (pc2[0] - pc[0]) * tg
                for r in rects[i]:
                    if r[0] <= pc2[0] <= r[0] + BLS and r[1] <= y <= r[1] + BLS:
                        tobreak = True
                        break
                if tobreak:
                    xdist = (pc2[0] - pc[0]) / cs
                    break
                xdist = st.raylen + BLS
                pc2[0] += sgn[0] * BLS
            tobreak = False
            for _ in range(size[1] // BLS):
                x = pc[0] + (pc2[1] - pc[1]) / tg
                for r in rects[i]:
                    if r[0] <= x <= r[0] + BLS and r[1] <= pc2[1] <= r[1] + BLS:
                        tobreak = True
                        break
                if tobreak:
                    ydist = (pc2[1] - pc[1]) / sn
                    break
                ydist = st.raylen + BLS
                pc2[1] += sgn[1] * BLS
            tobreak = False
            if xdist != st.raylen + BLS or ydist != st.raylen + BLS:
                dists[i][rayn] = abs(round(min(xdist, ydist) * optcos(fov - rayn * step)))
            else:
                dists[i][rayn] = 0
            if dists[i][rayn]:
                c = int(255 / (1 + dists[i][rayn] * 0.01))
                hg = k / dists[i][rayn]
                pg.draw.rect(layers[i], (c, c, c), (rayn * (size[0] // st.rays), size[1] // 2 - int(hg / 2), (size[0] // st.rays), int(hg)))
    screen.blit(layers[1], (0, 0))
    for i in range(4):
        if pressed[i]:
            plr.update(optcos(angle - radians(90 * i)) * tick / 10, optsin(angle - radians(90 * i)) * tick / 10)
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
            angle += radians(i.pos[0] - size[0] // 2) / 2
            if angle >= 2 * PI:
                angle = 0
            elif angle < 0:
                angle = 2 * PI
            pg.mouse.set_pos(size[0] // 2, size[1] // 2)