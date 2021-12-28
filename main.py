import pygame as pg
from Player import Player
from Settings import Settings


BLSIZE = (50, 50)


pg.init()
run = True
screen = pg.display.set_mode(size := (1000, 600))
pg.display.set_caption('WOAAAAH WHAT IS THIS MONSTER!!!')
layers = [pg.Surface(size) for _ in range(10)]
plr, obj = [pg.sprite.Group() for _ in range(2)]
Player(BLSIZE, size, plr)
st = Settings('Settings.txt')
print(st.fov)
while run:
    screen.fill((0, 0, 0))
    for i in layers:
        i.fill((0, 0, 0))
        plr.draw(i)
    screen.blit(layers[1], (0, 0))
    pg.display.flip()
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run = False
