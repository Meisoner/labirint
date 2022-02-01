from Player import Player
from Enemy import *
from Block import *
from Utilites import *
from Generator import labirint
from Texture import Texture
import os
import pygame
import sys
import datetime


def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        # image = image.convert_alpha()
        pass
    return image


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Счастливых вам голодных игр))"]

    fon = pygame.transform.scale(load_image('data/start.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color(180, 150, 230))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    f = True

    while f:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f = False
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                f = False
                return None
        pygame.display.flip()


# Создаёт новый уровень.
def new_location(endpos):
    global level, speccoord, spectexture, stset, objs, block_image, allrects, rects
    level += 1
    x, y = endpos
    spectexture += [Texture('data/txtr.png', 1000, 'Вход ->\nУровень ' + str(level))]
    speccoord += [(x + 1, y + 1)]
    stset = set(speccoord)
    lab2, nend = labirint(st.lablen, (1, 0))
    nend = (nend[0] + x - 1, nend[1] + y + 1)
    for nx in range(st.lablen):
        for ny in range(st.lablen):
            if lab2[nx][ny]:
                Block(objs, block_image, nx + x - 1, ny + y + 1)
    allrects = set(rects)
    return nend


# Конечное окно.
def endd():
    global results
    intro_text = ["ПОЖИЛИ...", ""
                               "И ХВАТИТ)))"]
    if results:
        with open('results.txt', 'a') as f:
            f.write(str(datetime.datetime.now()) + '\n')
            intro_text += ['Результаты:']
            count_average = False
            for num, i in enumerate(results):
                if not count_average:
                   intro_text += [str(num + 1) + ' ур. - ' + str(i) + ' секунд']
                f.write(str(num + 1) + ' level - ' + str(i) + ' seconds\n')
                if num == 7:
                    count_average = True
            if count_average:
                average = sum(results[7:]) // (len(results) - 7)
                intro_text += ['...и ещё ' + str(len(results) - 8) + ' ур., среднее время: ' +
                               str(average) + ' секунд']
    fon = pygame.transform.scale(load_image('data/end.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 120
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    f = True

    while f:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f = False
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                exit()
                return None
        pygame.display.flip()


size = WIDTH, HEIGHT = (1000, 600)

BLS = st.BLS
ENS = 20

pg.init()
screen = pg.display.set_mode(size)
texture = Texture('data/txtr.png', 1000)
pg.mouse.set_visible(False)
run, tobreak = True, False
pg.display.set_caption('lol')
start_screen()
objs = pg.sprite.Group()
dists, vsblocks = [0] * st.rays, [[]] * st.rays
endists, vsens = [0] * st.rays, [[]] * st.rays
plrs, enms = [pg.sprite.Group() for _ in range(2)]
layer = pg.Surface(size)
plr = Player(plrs)
fov = origfov = radians(st.fov)
step = fov / st.rays
angle = 0
clock = pg.time.Clock()
pressed = [False] * 4
keys = [pg.K_w, pg.K_a, pg.K_s, pg.K_d]
block_image = pg.Surface((BLS, BLS))
pg.draw.rect(block_image, (255, 0, 255), (0, 0, BLS, BLS))
enemy_image = pg.Surface((BLS, BLS))
pg.draw.rect(enemy_image, (255, 0, 0), (0, 0, BLS, BLS))
lb, end = labirint(st.lablen, (1, 0))
end = (end[0] + 1, end[1] + 1)
for x in range(st.lablen):
    for y in range(st.lablen):
        if lb[x][y]:
            Block(objs, block_image, x + 1, y + 1)
dopblocks = [(3, 0), (3, -1), (3, -2), (2, -2), (1, -2), (1, 0), (1, -1)]
for x, y in dopblocks:
    Block(objs, block_image, x, y)
xdist, ydist = 0, 0
k = BLS * st.rays / (2 * math.tan(fov / 2))
allrects = set(rects)
midray, can_attack, monster_drawn = st.rays // 2, False, False
monster, xm, ym, fm = [False] * 4
background = pg.transform.scale(pg.image.load('data/BG.png'), size)
speed, df = 10, 0
da0, da1 = 0, 0
yangle = PI
level = 1
spectexture, speccoord = [Texture('data/txtr.png', 1000, 'Вход ->\nУровень 1')], [(3, 1)]
stset = set(speccoord)
blockx, blocky = (0, 0), (0, 0)
lastend = end
end = new_location(end)
results = []
time_on_level = 0
pg.mixer.music.load('data/music.mp3')
pg.mixer.music.play(-1)
while run:
    tick = clock.tick()
    time_on_level += tick / 1000
    screen.blit(background, (0, 0))
    draw_floor(screen, size, yangle)
    pc = plr.get_centre()
    enemyset = set(enemy_rects)
    layer.fill((0, 0, 0))
    objs.draw(layer)
    plrs.draw(layer)
    for rayn in range(st.rays):
        # Вычисление тригонометрических функций для текущего угла взгляда игрока.
        sn = optsin(angle - fov + rayn * step)
        if not sn:
            sn = 10 ** -5
        cs = optcos(angle - fov + rayn * step)
        if not cs:
            cs = 10 ** -5
        tg = sn / cs
        # Вычисление округлённых координат игрока на клеточном поле.
        pc2 = [i - i % BLS for i in pc]
        # Вычисление типов углов.
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
            # Вычисление предположительной точки пересечентя блока с лучом.
            y = pc[1] + (pc2[0] - pc[0]) * tg
            x = pc2[0] + sgn[0]
            # Проверка наличия такого блока.
            if (x - x % BLS, y - y % BLS) in allrects:
                tobreak = True
                xdist = (pc2[0] - pc[0]) / cs
                da0 = pc[1] + xdist * sn
                blockx = int(x / BLS), int(da0 / BLS)
                break
            for r in enemyset:
                if not r:
                    continue
                if r[0] <= x <= r[0] + BLS and r[1] <= y <= r[1] + BLS:
                    enxdist = (pc2[0] - pc[0]) / cs
                    xm = r
                    break
            if tobreak:
                break
            xdist = st.raylen + BLS
            pc2[0] += sgn[0] * BLS
        tobreak = False
        for _ in range(size[1] // BLS):
            # Аналогично для другой оси.
            x = pc[0] + (pc2[1] - pc[1]) / tg
            y = pc2[1] + sgn[1]
            if (x - x % BLS, y - y % BLS) in allrects:
                tobreak = True
                ydist = (pc2[1] - pc[1]) / sn
                da1 = pc[0] + ydist * cs
                blocky = int(da1 / BLS), int(y / BLS)
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
            # Выччисление итогового расстояния до блока.
            final = min(xdist, ydist) * optcos(fov / 2 - rayn * step)
            if final:
                height = k / final
                if xdist < ydist:
                    block = blockx
                    if block in stset:
                        for n in range(len(speccoord)):
                            if speccoord[n] == block:
                                this_texture = spectexture[n].get(da0, height)
                    else:
                        this_texture = texture.get(da0, height)
                else:
                    block = blocky
                    if block in stset:
                        for n in range(len(speccoord)):
                            if speccoord[n] == block:
                                this_texture = spectexture[n].get(da1, height)
                    else:
                        this_texture = texture.get(da1, height)
                # Рисование отрезка на текущем луче по заданным параметрам.
                draw(screen, size, height, rayn, this_texture, yangle)
                # print(block)
        if enxdist != st.raylen + ENS or enydist != st.raylen + ENS:
            enfinal = min(enxdist, enydist) * optcos(fov / 2 - rayn * step)
            if enfinal:
                colour = int(120 / (1 + enfinal * 0.01))
                height = k / (1.5 * enfinal)
                draw_enemy(screen, size, height, colour, rayn)
                if enxdist < enydist:
                    fm = xm
                else:
                    fm = ym
                if rayn == midray and enfinal <= 100:
                    monster_drawn = True
    if monster_drawn:
        can_attack = True
        monster_drawn = False
    else:
        can_attack = False
    for i in range(4):
        if pressed[i]:
            plr.update(optcos(angle - radians(90 * i + 40)) * tick / speed,
                       optsin(angle - radians(90 * i + 40)) * tick / speed, objs, False)
            break
    pg.display.flip()
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run = False
        elif i.type == pg.KEYDOWN:
            if i.key == pg.K_ESCAPE:
                run = False
                endd()
            elif i.key == pg.K_LCTRL:
                speed -= 5
                df = 10
            else:
                for key in range(4):
                    if i.key == keys[key]:
                        pressed[key] = True
        elif i.type == pg.KEYUP:
            if i.key == pg.K_LCTRL:
                speed += 5
                df = -10
            else:
                for key in range(4):
                    if i.key == keys[key]:
                        pressed[key] = False
        elif i.type == pg.MOUSEMOTION:
            angle += radians(i.pos[0] - size[0] // 2) / 2
            if angle >= 2 * PI:
                angle = 0
            elif angle < 0:
                angle = 2 * PI
            yangle += radians(i.pos[1] - size[1] // 2) / 2
            if yangle >= 7:
                yangle = 7
            elif yangle < -1:
                yangle = -1
            pg.mouse.set_pos(size[0] // 2, size[1] // 2)
        elif i.type == pg.MOUSEBUTTONDOWN:
            if can_attack:
                enemies[enemy_rects.index(fm)].terminate()
    # Динамическое изменение поля зрения во время спринта.
    if df > 0:
        df -= tick / 20
        fov = origfov + radians(10 - int(df))
        k = BLS * st.rays / (2 * math.tan(fov / 2))
        if df < 1:
            df = 0
    elif df < 0:
        df += tick / 20
        fov = origfov + radians(-1 * int(df))
        k = BLS * st.rays / (2 * math.tan(fov / 2))
        if df > -1:
            df = 0
    if plr.get_block() == lastend:
        lastend = end
        end = new_location(end)
        results += [round(time_on_level)]
        time_on_level = 0