import pygame as pg
from objects import *
from model import *
from game_process import *
from vis import *
from random import randint

pg.init()

FPS = 30
WIDTH = 800
HEIGHT = 800
screen = pg.display.set_mode((WIDTH, HEIGHT))
calculate_scale_factor(800)

pg.display.update()
clock = pg.time.Clock()
finished = False

game_state = 3                      # Состояние игры
landing_time = 1                    # Время приземления ракеты
shift_time = 0.5                    # Время смещения экрана
min_starting_takeoff_force = 60     # Минимальная начальная скорость ракеты
speed_gain_per_second = 20          # Прирост скорости за секунду, пока нажат пробел
comet_time = 5                      # Время между пролетом комет

distance = 0
SPACE_pressed = 0
takeoff_force = min_starting_takeoff_force

r_min, r_max = 30, 70

rocket = Rocket(screen, 400, 600, 'images/rocket.png')
planet = Planet(screen, 400, 710, 50, randint(0, 1) * 2 - 1, 'images/planet.png')
next_planet = Planet(screen, randint(100, 700), 200, randint(r_min, r_max), randint(0, 1) * 2 - 1, 'images/planet.png')
planets = [planet, next_planet]
comet = Comet(screen, 0, 0, 10, 10, 'images/comet.png')

while not finished:
    dt = 1 / FPS
    clock.tick(FPS)
    screen.fill((255, 255, 255))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True

    if game_state == 0:             # Полет
        collision = pg.sprite.collide_mask(rocket, next_planet)
        if not collision:
            calculate_force(rocket, planets)
            rocket.move(dt)
        else:
            game_state = 1

    if game_state == 1:             # Приземление
        is_rotated = rocket_landing(rocket, next_planet, dt, landing_time)
        if is_rotated:
            t = 0
            prev_planet = planet
            planet = next_planet
            next_planet = Planet(screen, randint(100, 700), -200, randint(r_min, r_max), randint(0, 1) * 2 - 1, 'images/planet.png')
            planets = [prev_planet, planet, next_planet]
            game_state = 2

    if game_state == 2:             # Смещение экрана
        if t < shift_time:
            screen_shift([rocket] + planets, shift_time, dt)
            t += dt
        else:
            planets.pop(0)
            distance = 0
            SPACE_pressed = 0
            takeoff_force = min_starting_takeoff_force
            game_state = 3

    if game_state == 3:             # Ожидение полета
        distance = math.hypot(planet.rect.centerx - rocket.rect.centerx, planet.rect.centery - rocket.rect.centery) if distance == 0 else distance
        rocket_rotation(rocket, planet, dt, planet.period, distance)
        keystate = pg.key.get_pressed()
        if keystate[pg.K_SPACE]:
            SPACE_pressed = 1
            takeoff_force += dt * speed_gain_per_second
        elif SPACE_pressed == 1:
            rocket_launch(rocket, takeoff_force)
            game_state = 0         # Запуск ракеты

    for obj in planets:
        planet_rotation(obj, dt, planet.period)

    for obj in planets + [rocket] + [comet]:
        blitRotate(screen, obj.initial_image, (obj.rect.x, obj.rect.y), obj.angle)

    comet.move(dt)
    pg.draw.circle(screen, (0, 0, 0), (rocket.rect.centerx, rocket.rect.centery), 2)
    pg.draw.circle(screen, (0, 0, 0), (planet.rect.centerx, planet.rect.centery), 2)

    pg.display.update()

pg.quit()
