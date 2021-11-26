import pygame as pg
from objects import *
from model import *
from game_process import *

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
next_planet = Planet(300, 100, 'images/planet.png')
all_sprites = pg.sprite.Group()
all_sprites.add(rocket, planet)
planets = [planet, next_planet]

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

    collision = pg.sprite.spritecollide(rocket, planets, False)
    if not collision:
        rocket.move(dt)
        calculate_force(rocket, all_sprites)
        image = rocket.rotate()
    else:
        image = rocket_landing(rocket, planet)
        next_planet = Planet(300, 100, 'images/planet.png')
        planets = planets[1:] + [next_planet]

    screen.blit(image, rocket.rect)
    for x in planets:
        screen.blit(x.image, x.rect)
    all_sprites.update()
    pg.display.update()

pg.quit()
