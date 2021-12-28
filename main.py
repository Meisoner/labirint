import pygame as pg


BLSIZE = (50, 50)


class Player(pg.sprite.Sprite):
    img = pg.Surface(BLSIZE)
    pg.draw.rect(img, (255, 255, 255), (0, 0, 50, 50))

    def __init__(self):
        global plr, size
        super().__init__(plr)
        self.image = Player.img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = size[0] // 2 - self.rect.size[0] // 2, size[1] // 2 - self.rect.size[1] // 2


pg.init()
run = True
screen = pg.display.set_mode(size := (1000, 600))
pg.display.set_caption('WOAAAAH WHAT IS THIS MONSTER!!!')
layers = [pg.Surface(size) for _ in range(10)]
plr, obj = [pg.sprite.Group() for _ in range(2)]
Player()
st = dict()
with open('settings.txt') as f:
    for i in f.read().split('\n'):
        s, arg = i.split()
        if arg.isnumeric():
            st[s] = int(arg)
        elif arg.replace('.', '').isnumeric():
            st[s] = float(arg)
        else:
            st[s] = arg
print(st)
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
