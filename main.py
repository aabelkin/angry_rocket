import pygame as pg
from objects import *
from model import *

pg.init()

FPS = 30
WIDTH = 800
HEIGHT = 800
screen = pg.display.set_mode((WIDTH, HEIGHT))

pg.display.update()
clock = pg.time.Clock()
finished = False

rocket = Rocket(WIDTH / 2, HEIGHT / 2, 'images/rocket.png')
planet = Planet(200, 200, 'images/planet.png')
all_sprites = pg.sprite.Group()
all_sprites.add(rocket, planet)
while not finished:
    dt = 1 / FPS
    clock.tick(FPS)
    screen.fill((255, 255, 255))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        if event.type == pg.MOUSEMOTION:
            rocket.targetting(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            pass

    rocket.move(dt)
    calculate_force(rocket, all_sprites)
    image = rocket.rotate()
    print(rocket.Fx, rocket.Fy)

    screen.blit(image, rocket.rect)
    screen.blit(planet.image, planet.rect)
    all_sprites.update()
    pg.display.update()

pg.quit()
