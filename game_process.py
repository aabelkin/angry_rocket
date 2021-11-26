import pygame as pg
import math

def rocket_landing(rocket, planet):
    t = -(planet.x - rocket.rect.x) / (planet.y - rocket.rect.y)
    if t > 0:
        p_angle = math.atan(t) / 2 / math.pi * 360 + 180
    else:
        p_angle = math.atan(t) / 2 / math.pi * 360
    rocket.angle = 180 + p_angle - rocket.angle
    return rocket.rotate()
