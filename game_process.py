import pygame as pg
import math

def blitRotate(surf, image, topleft, angle):
    """ Изменение угла поворота изображения относительно центра на angle
    """
    rotated_image = pg.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect.topleft)
    pg.draw.rect(surf, (255, 0, 0), new_rect, 2)

def rocket_landing(rocket, planet):
    """ Поворот ракеты при приземлении
    """
    is_rotated = False
    t = (planet.rect.centerx - rocket.rect.centerx) / (planet.rect.centery - rocket.rect.centery)
    if planet.rect.centerx - rocket.rect.centerx > 0 :
        if planet.rect.centery - rocket.rect.centery > 0:
            planet_angle = 180 - math.degrees(math.atan(t))
        else:
            planet_angle = math.degrees(math.atan(-t)) + 180
    else:
        if planet.rect.centery - rocket.rect.centery > 0:
            planet_angle = math.degrees(math.atan(-t)) - 180
        else:
            planet_angle = -math.degrees(math.atan(t))
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

def rocket_rotation(rocket, planet, dt, period, distance):
    """ Вращение приземленной ракеты за планетой
    """
    print(rocket.rect.centerx, rocket.rect.centery)
    rocket.rect.centerx = planet.rect.centerx + distance * math.sin(math.radians(rocket.angle))
    rocket.rect.centery = planet.rect.centery - distance * math.cos(math.radians(rocket.angle))
    rocket.angle += dt / period * 360
    if rocket.angle >= 180:
        rocket.angle -= 360

def planet_rotation(planet, dt, period):
    """ Вращение планеты вокруг своей оси
    """
    planet.angle += dt / period * 360
    if planet.angle >= 180:
        planet.angle -= 360
