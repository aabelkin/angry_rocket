import pygame as pg
import math

def rocket_landing(rocket, planet):
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
    if angle_difference < 0:
        angle = 180 + planet_angle
        print(angle, rocket.angle)
        if abs(rocket.angle - angle) > 1:
            rocket.angle += 1
    else:
        angle = 180 + rocket.angle + angle_difference
        if abs(rocket.angle - angle) > 1:
            rocket.angle += 1
