from Player import Player
from Enemy import *
from Block import *
from Utilites import *
from Generator import labirint


BLS = st.BLS
ENS = 20


pg.init()
pg.mouse.set_visible(False)
run, tobreak = True, False
screen = pg.display.set_mode(size := (1000, 600))
pg.display.set_caption('lol')
layers = [pg.Surface(size) for _ in range(st.maxheight)]
objs = [pg.sprite.Group() for _ in range(st.maxheight)]
dists, vsblocks = [0] * st.rays, [[]] * st.rays
endists, vsens = [0] * st.rays, [[]] * st.rays
plrs, enms = [pg.sprite.Group() for _ in range(2)]
plr = Player(plrs)
fov = radians(st.fov)
step = fov / st.rays
angle = 0
clock = pg.time.Clock()
pressed = [False] * 4
keys = [pg.K_w, pg.K_a, pg.K_s, pg.K_d]
block_image = pg.Surface((BLS, BLS))
pg.draw.rect(block_image, (255, 0, 255), (0, 0, BLS, BLS))
enemy_image = pg.Surface((BLS, BLS))
pg.draw.rect(enemy_image, (255, 0, 0), (0, 0, BLS, BLS))
lb = labirint(st.lablen, (5, 0))
for x in range(st.lablen):
    for y in range(st.lablen):
        if lb[x][y]:
            Block(objs[0], block_image, x, y, 0)
            Block(objs[1], block_image, x, y, 1)
# Block(objs[0], block_image, 3, 4, 0)
# Block(objs[0], block_image, 4, 4, 0)
en = Enemy(enms, 1, 2)
xdist, ydist = 0, 0
k = BLS * st.rays / (2 * math.tan(fov / 2))
allrects = set(rects[0])
midray, can_attack, monster_drawn = st.rays // 2, False, False
monster, xm, ym, fm = [False] * 4
while run:
    tick = clock.tick()
    screen.fill((0, 0, 0))
    pc = plr.get_centre()
    enms.update(tick / 1000, tick / 2000)
    enemyset = set(enemy_rects)
    print(enemy_rects)
#    for i in range(st.maxheight):
#        layers[i].fill((0, 0, 0))
#        objs[i].draw(layers[i])
#        plrs.draw(layers[i])
    for rayn in range(st.rays):
        sn = optsin(angle - fov + rayn * step)
        if not sn:
            sn = 10 ** -5
        cs = optcos(angle - fov + rayn * step)
        if not cs:
            cs = 10 ** -5
        tg = sn / cs
        pc2 = [(i // BLS) * BLS for i in pc]
        sgn = [1, 1]
        if cs < 0:
            sgn[0] = -1
        if sn < 0:
            sgn[1] = -1
        pc2[0] += BLS * ((sgn[0] + 1) // 2)
        pc2[1] += BLS * ((sgn[1] + 1) // 2)
        xbl, ybl, xen, yen = [[] for _ in range(4)]
        enydist, enxdist = st.raylen + ENS, st.raylen + ENS
        tobreak = False
        for _ in range(size[0] // BLS):
            y = pc[1] + (pc2[0] - pc[0]) * tg
            x = pc2[0] + sgn[0]
            if (x - x % BLS, y - y % BLS) in allrects:
                tobreak = True
                xdist = (pc2[0] - pc[0]) / cs
                break
            for r in enemyset:
                if not r:
                    continue
                if r[0] <= x <= r[0] + BLS and r[1] <= y <= r[1] + BLS:
#                    print(r, pc2, x)
                    enxdist = (pc2[0] - pc[0]) / cs
                    xm = r
                    break
            if tobreak:
                break
            xdist = st.raylen + BLS
            pc2[0] += sgn[0] * BLS
        tobreak = False
        for _ in range(size[1] // BLS):
            x = pc[0] + (pc2[1] - pc[1]) / tg
            y = pc2[1] + sgn[1]
            if (x - x % BLS, y - y % BLS) in allrects:
                tobreak = True
                ydist = (pc2[1] - pc[1]) / sn
                break
            for r in enemyset:
                if not r:
                    continue
                if r[0] <= x <= r[0] + BLS and r[1] <= y <= r[1] + BLS:
                    enydist = (pc2[1] - pc[1]) / sn
                    ym = r
                    break
            if tobreak:
                break
            ydist = st.raylen + BLS
            pc2[1] += sgn[1] * BLS
        if xdist != st.raylen + BLS or ydist != st.raylen + BLS:
            final = min(xdist, ydist) * optcos(fov / 2 - rayn * step)
            if final:
                colour = int(255 / (1 + final * 0.01))
                height = k / final
                draw(screen, size, height, colour, rayn)
        if enxdist != st.raylen + ENS or enydist != st.raylen + ENS:
            enfinal = min(enxdist, enydist) * optcos(fov / 2 - rayn * step)
            if enfinal:
                colour = int(120 / (1 + enfinal * 0.01))
                height = k / (1.5 * enfinal)
                draw_enemy(screen, size, height, colour, rayn)
                if rayn == midray and enfinal <= 100:
                    if enxdist < enydist:
                        fm = xm
                    else:
                        fm = ym
                    monster_drawn = True
#        if enxdist != st.raylen + ENS or enydist != st.raylen + ENS:
#            endists[rayn] = min(enxdist, enydist) * optcos(fov / 2 - rayn * step)
#            if enxdist < enydist:
#                vsens[rayn] = xen
#            else:
#                vsens[rayn] = yen
#        else:
#            endists[rayn] = 0
#    for rayn, dist in enumerate(endists):
#        if not dist:
#            continue
#        if vsens[rayn] in enemy_rects:
#            colour = int(120 / (1 + dist * 0.01))
#            height = k / (1.5 * dist)
#            draw_enemy(screen, size, height, colour, rayn)
#    for rayn, dist in enumerate(dists):
#        if not dist:
#            continue
#        drawing_layers = []
#        for layer in range(st.maxheight):
#            if vsblocks[rayn] in rects[layer]:
#                drawing_layers += [layer]
#        colour = int(255 / (1 + dist * 0.01))
#        height = k / dist
    if monster_drawn:
        can_attack = True
        monster_drawn = False
    else:
        can_attack = False
    for i in range(4):
        if pressed[i]:
            plr.update(optcos(angle - radians(90 * i + 40)) * tick / 10,
                       optsin(angle - radians(90 * i + 40)) * tick / 10)
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
        elif i.type == pg.MOUSEBUTTONDOWN:
            if can_attack:
                print(enemy_rects.index(fm))
                enemies[enemy_rects.index(fm)].terminate()