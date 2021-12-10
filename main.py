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

rocket = Rocket(screen, 600, 600, 'images/rocket.png')
planet = Planet(screen, 200, 200, 'images/planet.png')
next_planet = Planet(screen, 600, -200, 'images/planet.png')
all_sprites = pg.sprite.Group()
all_sprites.add(rocket, planet)
planets = [planet]

game_state = 0  # Состояние игры
shift_time = 0.5  # Время смещения экрана

while not finished:
    dt = 1 / FPS
    clock.tick(FPS)
    screen.fill((255, 255, 255))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        if event.type == pg.MOUSEMOTION:
            pass
        if event.type == pg.MOUSEBUTTONDOWN:
            pass

    if game_state == 0:     # Полет
        collision = pg.sprite.collide_mask(rocket, planet)
        if collision:
            game_state = 1
        else:
            calculate_force(rocket, planets)
            rocket.move(dt)
    if game_state == 1:     # Приземление
        is_rotated = rocket_landing(rocket, planet)
        if is_rotated:
            game_state = 2
            t = 0
    if game_state == 2:     # Смещение экрана
        if t < shift_time:
            screen_shift([rocket] + planets, shift_time, dt)
            t += dt
        else:
            game_state = 3
    if game_state == 3:     # Ожидение полета и запуск
        rocket.angle += 1
        planet.angle += 1

    pg.draw.circle(screen, (0, 0, 0), (rocket.rect.centerx, rocket.rect.centery), 2)
    pg.draw.circle(screen, (0, 0, 0), (planet.rect.centerx, planet.rect.centery), 2)
    blitRotate(screen, planet.initial_image, (planet.rect.x, planet.rect.y), -planet.angle)
    blitRotate(screen, rocket.initial_image, (rocket.rect.x, rocket.rect.y), -rocket.angle)
    pg.display.update()

pg.quit()
