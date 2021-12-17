import pygame as pg
import math

def blitRotate(surf, image, topleft, angle):
    """Поворачивает изображение относительно его центра на заданный угол
    и рисует его на поверхности

    Параметры
    ----------
    surf : pygame.Surface
        экран, на котором рисуется изображение
    image : pygame.Surface
        поверхность с изображением
    topleft: tuple
        пара координат x и y верхнего левого угла изображения
    angle : float
        угол поворота изображения
    """
    rotated_image = pg.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect.topleft)

def rocket_landing(rocket, planet, dt, landing_time):
    """Реализует поворот ракеты при приземлении на планету
    за время dt и возвращает True, если приземление завершено,
    иначе False

    Параметры
    ----------
    rocket : Sprite
        ракета
    planet : Sprite
        планета
    dt: float
        время небольшого поворота
    landing_time : list
        время приземления
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

def screen_shift(objects, shift, shift_time, dt):
    """Сдвигает экран при приземлении на следующую планету
    на небольшое расстояние за малое время dt

    Параметры
    ----------
    objects : list
        объекты, которые необходимо сдвинуть
    shift : int
        сдвиг в пикселях
    shift_time: float
        время сдвига
    dt : float
        время небольшого сдвига
    """
    for x in objects:
        x.rect.y += shift * dt / shift_time

def rocket_rotation(rocket, planet, dt, period, distance):
    """Вращение приземленной на планету ракеты относительно центра планеты

    Параметры
    ----------
    rocket : Sprite
        ракета
    planet : Sprite
        планета
    period: float
        период вращения вокруг центра планеты
    distance: int
        расстояние от центра ракеты до центра планеты
    dt : float
        время небольшого вращения
    """
    rocket.rect.centerx = planet.rect.centerx - distance * math.sin(math.radians(rocket.angle))
    rocket.rect.centery = planet.rect.centery - distance * math.cos(math.radians(rocket.angle))
    rocket.angle += dt / period * 360 * planet.direction
    if rocket.angle <= -180:
        rocket.angle += 360
    if rocket.angle >= 180:
        rocket.angle -= 360

def obj_rotation(obj, dt, period):
    """Вращение объекта вокруг своей оси

    Параметры
    ----------
    obj : Sprite
        объект
    period: float
        период вращения объекта вокруг центра
    dt : float
        время небольшого вращения
    """
    obj.angle += dt / period * 360 * obj.direction
    if obj.angle <= -180:
        obj.angle += 360
    if obj.angle >= 180:
        obj.angle -= 360

def rocket_launch(rocket, takeoff_force):
    """Задает начальные скорости ракеты по осям x и y во время ее запуска

    Параметры
    ----------
    rocket : Sprite
        ракета
    takeoff_force : Sprite
        модуль скорости ракеты
    """
    rocket.Vx = -takeoff_force * math.sin(math.radians(rocket.angle))
    rocket.Vy = -takeoff_force * math.cos(math.radians(rocket.angle))
