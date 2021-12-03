import pygame as pg
from objects import *
from model import *
from game_process import *
from vis import *

pg.init()

FPS = 30
WIDTH = 800
HEIGHT = 800
screen = pg.display.set_mode((WIDTH, HEIGHT))
calculate_scale_factor(400)

pg.display.update()
clock = pg.time.Clock()
finished = False

rocket = Rocket(screen, WIDTH * 3 / 4, HEIGHT * 3 / 4, 'images/rocket.png')
planet = Planet(screen, 200, 200, 'images/planet.png')
next_planet = Planet(screen, 400, 100, 'images/planet.png')
all_sprites = pg.sprite.Group()
all_sprites.add(rocket, planet)
planets = [planet, next_planet]

game_state = 0  # Состояние игры
shift_time = 1  # Время смещения экрана

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

    if game_state == 0:     # Полет
        collision = pg.sprite.collide_mask(rocket, planet)
        if collision:
            game_state = 1
        else:
            calculate_force(rocket, all_sprites)
            rocket.move(dt)
            rocket.flight_rotation()
    if game_state == 1:     # Приземление
        is_rotated = rocket_landing(rocket, planet)
        if is_rotated:
            game_state = 2
    if game_state == 2:     # Смещение экрана
        is_shifted = screen_shift()
        if is_shifted:
            game_state = 3
    if game_state == 3:     # Ожидение полета и запуск
        pass
        #next_planet = Planet(screen, 300, 100, 'images/planet.png')
        #planets = planets[1:] + [next_planet]

    rocket.draw()
    for x in planets:
        x.draw()
    pg.display.update()

pg.quit()
