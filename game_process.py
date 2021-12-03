import pygame as pg
import math

def rocket_landing(rocket, planet):
    """ Поворот ракеты при приземлении
    """
    is_rotated = False
    t = (planet.rect.x - rocket.rect.x) / (planet.rect.y - rocket.rect.y)
    if planet.rect.x - rocket.rect.x > 0 :
        if planet.rect.y - rocket.rect.y > 0:
            planet_angle = 180 - math.atan(t) / 2 / math.pi * 360
        else:
            planet_angle = math.atan(-t) / 2 / math.pi * 360 + 180
    else:
        if planet.rect.y - rocket.rect.y > 0:
            planet_angle = math.atan(-t) / 2 / math.pi * 360 - 180
        else:
            planet_angle = -math.atan(t) / 2 / math.pi * 360
    angle_difference = planet_angle - rocket.angle
    angle = 180 + planet_angle
    if angle_difference < 0:
        if abs(rocket.angle - angle) > 1:
            rocket.angle += 1
        else:
            is_rotated = True
    else:
        if abs(rocket.angle - angle) > 1:
            rocket.angle -= 1
        else:
            is_rotated = True
    return is_rotated

def screen_shift(objects, shift_time, dt):
    """ Сдвиг всех объектов и фона вниз за время shift_time
    """
    for x in objects:
        x.rect.y += 400 * dt / shift_time
