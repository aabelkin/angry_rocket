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
calculate_scale_factor(800)

pg.display.update()
clock = pg.time.Clock()
finished = False

rocket = Rocket(screen, 600, 600, 'images/rocket.png')
prev_planet = Planet(screen, 600, 690, 'images/planet.png')
planet = Planet(screen, 200, 200, 'images/planet.png')
next_planet = Planet(screen, 600, -200, 'images/planet.png')
planets = [prev_planet, planet]

game_state = 0                      # Состояние игры
landing_time = 1                    # Время приземления ракеты
shift_time = 0.5                    # Время смещения экрана
min_starting_takeoff_force = 70     # Минимальная начальная скорость ракеты
speed_gain_per_second = 10          # Прирост скорости за секунду, пока нажат пробел

while not finished:
    dt = 1 / FPS
    clock.tick(FPS)
    screen.fill((255, 255, 255))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True

    if game_state == 0:             # Полет
        collision = pg.sprite.collide_mask(rocket, planet)
        if collision:
            game_state = 1
        else:
            calculate_force(rocket, planets)
            rocket.move(dt)

    if game_state == 1:             # Приземление
        is_rotated = rocket_landing(rocket, planet, dt, landing_time)
        if is_rotated:
            game_state = 2
            t = 0
            planets += [next_planet]

    if game_state == 2:             # Смещение экрана
        if t < shift_time:
            screen_shift([rocket] + planets, shift_time, dt)
            t += dt
        else:
            planets.pop(0)
            game_state = 3
            distance = 0
            SPACE_pressed = 0
            takeoff_force = min_starting_takeoff_force

    if game_state == 3:             # Ожидение полета
        distance = math.hypot(planet.rect.centerx - rocket.rect.centerx, planet.rect.centery - rocket.rect.centery) if distance == 0 else distance
        rocket_rotation(rocket, planet, dt, planet.period, distance)
        keystate = pg.key.get_pressed()
        if keystate[pg.K_SPACE]:
            SPACE_pressed = 1
            takeoff_force += dt * speed_gain_per_second
        elif SPACE_pressed == 1:
            rocket_launch(rocket, takeoff_force)
            prev_planet = planet
            planet = next_planet
            next_planet = Planet(screen, 200, -200, 'images/planet.png')
            game_state = 0         # Запуск ракеты

    for obj in planets:
        planet_rotation(obj, dt, planet.period)

    for obj in planets + [rocket]:
        blitRotate(screen, obj.initial_image, (obj.rect.x, obj.rect.y), obj.angle)

    pg.draw.circle(screen, (0, 0, 0), (rocket.rect.centerx, rocket.rect.centery), 2)
    pg.draw.circle(screen, (0, 0, 0), (planet.rect.centerx, planet.rect.centery), 2)

    pg.display.update()

pg.quit()
