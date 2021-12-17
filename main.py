import pygame as pg
from objects import *
from model import *
from game_process import *
from random import uniform, randint

pg.init()

FPS = 30
WIDTH = 800
HEIGHT = 800
screen = pg.display.set_mode((WIDTH, HEIGHT))

pg.display.update()
clock = pg.time.Clock()
font = pg.font.Font(None, 70)
bg = Background(WIDTH, HEIGHT, WIDTH / 2)
bg_next = Background(WIDTH, HEIGHT, -WIDTH / 2)
bgs = [bg, bg_next]
finished = False
game_over = 0

game_state = 3                      # Состояние игры
landing_time = 1                    # Время приземления ракеты
shift_time = 0.5                    # Время смещения экрана
min_starting_takeoff_force = 120    # Минимальная начальная скорость ракеты
speed_gain_per_second = 20          # Прирост скорости за секунду, пока нажат пробел
hp = 3                              # Количество жизней
score = 0

distance = 0
SPACE_pressed = 0
takeoff_force = min_starting_takeoff_force

planet_r_min, planet_r_max = 30, 60
comet_r_min, comet_r_max = 20, 30

rocket = Rocket(screen, 400, 600, 'images/rocket.png')
planet = Planet(screen, 400, 710, 50, randint(0, 1) * 2 - 1)
next_planet = Planet(screen, randint(100, 700), 100, randint(planet_r_min, planet_r_max), randint(0, 1) * 2 - 1)
planets = [planet, next_planet]
tmp = uniform(0.3, 0.7)
next_comet_x = tmp * (next_planet.rect.x + next_planet.r) + (1 - tmp) * (planet.rect.x + planet.r)
next_comet_y = tmp * (next_planet.rect.y + next_planet.r) + (1 - tmp) * (planet.rect.y + planet.r)
comet = Comet(screen, next_comet_x, next_comet_y, randint(comet_r_min, comet_r_max), 'images/comet.png')
comets = [comet]

while not finished:
    dt = 1 / FPS
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True

    for obj in bgs:
        screen.blit(obj.image, (obj.rect.x, obj.rect.y))

    if bg.rect.y >= WIDTH:
        for obj in bgs:
            obj.rect.y -= WIDTH

    if game_state == 0:             # Полет
        rocket_planet_collision = pg.sprite.collide_mask(rocket, next_planet)
        if not rocket_planet_collision:
            calculate_force(rocket, planets + [comet])
            rocket.move(dt)
        else:
            score += 1
            hp += 1
            game_state = 1

    if game_state == 1:             # Приземление
        is_rotated = rocket_landing(rocket, next_planet, dt, landing_time)
        if is_rotated:
            t = 0
            prev_planet = planet
            planet = next_planet
            next_planet = Planet(screen, randint(100, 700), -400, randint(planet_r_min, planet_r_max), randint(0, 1) * 2 - 1)
            planets = [prev_planet, planet, next_planet]

            tmp = uniform(0.3, 0.7)
            next_comet_x = tmp * (next_planet.rect.x + next_planet.r) + (1 - tmp) * (planet.rect.x + planet.r)
            next_comet_y = tmp * (next_planet.rect.y + next_planet.r) + (1 - tmp) * (planet.rect.y + planet.r)
            next_comet = Comet(screen, next_comet_x, next_comet_y, randint(comet_r_min, comet_r_max), 'images/comet.png')
            comets = [comet, next_comet]
            game_state = 2

    if game_state == 2:             # Смещение экрана
        if t < shift_time:
            screen_shift(planets + comets + [rocket], 500, shift_time, dt)
            screen_shift(bgs, 100, shift_time, dt)
            t += dt
        else:
            planets.pop(0)
            comet = next_comet
            comets.pop(0)
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
            game_state = 0          # Запуск ракеты

    comet_rocket_collision = pg.sprite.collide_mask(comet, rocket)
    if comet_rocket_collision:
        hp -= 1
        SPACE_pressed = 0
        screen.fill((255, 0, 0))
        game_state = 3

    if (rocket.rect.centerx < 0 or rocket.rect.centerx > WIDTH or\
       rocket.rect.centery < 0 or rocket.rect.centery > HEIGHT):
        if hp != 0:
            hp -= 1
            SPACE_pressed = 0
            screen.fill((255, 0, 0))
            game_state = 3
        else:
            finished = True

    if hp == 0:
        game_over = 1
        finished = True

    for obj in planets:
        obj_rotation(obj, dt, obj.period)

    for obj in planets + [rocket]:
        blitRotate(screen, obj.initial_image, (obj.rect.x, obj.rect.y), obj.angle)

    for obj in comets:
        screen.blit(obj.image, obj.rect)

    screen.blit(pg.transform.scale(pg.image.load('images/hp.png').convert_alpha(), (50, 50)), (0, 0))
    screen.blit(pg.transform.scale(pg.image.load('images/score.png').convert_alpha(), (50, 50)), (700, 0))
    screen.blit(font.render(str(hp), True, (255, 255, 255)), (50, 5))
    screen.blit(font.render(str(score), True, (255, 255, 255)), (750, 5))
    pg.display.update()

finished = 0

while not finished and game_over:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True

    screen.blit(pg.transform.scale(pg.image.load('images/background.jpg').convert_alpha(), (WIDTH, HEIGHT)), (0, 0))
    screen.blit(font.render('SCORE: ' + str(score), True, (255, 255, 255)), (300, 350))
    screen.blit(font.render('GAME OVER', True, (255, 255, 255)), (250, 300))
    pg.display.update()

pg.quit()
