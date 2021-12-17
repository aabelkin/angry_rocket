import pygame as pg
import math

def blitRotate(surf, image, topleft, angle):
    """ Изменение угла поворота изображения относительно центра на angle
    """
    rotated_image = pg.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect.topleft)

def rocket_landing(rocket, planet, dt, landing_time):
    """ Поворот ракеты при приземлении
    """
    is_rotated = False
    if planet.rect.centery - rocket.rect.centery == 0:
        if planet.rect.centerx - rocket.rect.centerx > 0:
            angle = 90
        else:
            angle = -90
    else:
        t = (planet.rect.centerx - rocket.rect.centerx) / (planet.rect.centery - rocket.rect.centery)
        if planet.rect.centerx - rocket.rect.centerx > 0 :
            if planet.rect.centery - rocket.rect.centery > 0:
                angle = math.degrees(math.atan(t))
            else:
                angle = 180 - math.degrees(math.atan(-t))
        else:
            if planet.rect.centery - rocket.rect.centery > 0:
                angle = -math.degrees(math.atan(-t))
            else:
                angle = math.degrees(math.atan(t)) - 180
    angle_difference = rocket.angle - angle
    d_angle = dt / landing_time * 360
    if angle_difference < 0:
        if abs(rocket.angle - angle) > d_angle:
            rocket.angle += d_angle
        else:
            is_rotated = True
    else:
        if abs(rocket.angle - angle) > d_angle:
            rocket.angle -= d_angle
        else:
            is_rotated = True
    return is_rotated

def screen_shift(objects, shift_time, dt):
    """ Сдвиг всех объектов и фона вниз за время shift_time
    """
    for x in objects:
        x.rect.y += 500 * dt / shift_time

def rocket_rotation(rocket, planet, dt, period, distance):
    """ Вращение приземленной ракеты за планетой
    """
    rocket.rect.centerx = planet.rect.centerx - distance * math.sin(math.radians(rocket.angle))
    rocket.rect.centery = planet.rect.centery - distance * math.cos(math.radians(rocket.angle))
    rocket.angle += dt / period * 360 * planet.direction
    if rocket.angle <= -180:
        rocket.angle += 360
    if rocket.angle >= 180:
        rocket.angle -= 360

def obj_rotation(obj, dt, period):
    """ Вращение планеты вокруг своей оси
    """
    obj.angle += dt / period * 360 * obj.direction
    if obj.angle <= -180:
        obj.angle += 360
    if obj.angle >= 180:
        obj.angle -= 360

def rocket_launch(rocket, takeoff_force):
    """ Запуск ракеты со скоростью takeoff_force
    """
    rocket.Vx = -takeoff_force * math.sin(math.radians(rocket.angle))
    rocket.Vy = -takeoff_force * math.cos(math.radians(rocket.angle))