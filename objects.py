import pygame as pg
import math
from vis import *
import random

def blitRotate(surf, image, topleft, angle):

    rotated_image = pg.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)
    pg.draw.rect(surf, (255, 0, 0), new_rect, 2)

class Rocket(pg.sprite.Sprite):
    def __init__(self, screen, x, y, filename):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.w = 40
        self.h = 80
        self.initial_image = pg.transform.scale(pg.image.load(filename).convert_alpha(), (self.w, self.h))
        self.image = self.initial_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.m = 10**5
        self.rect.x = x
        self.rect.y = y
        self.Fx = 0
        self.Fy = 0
        self.Vx = -30
        self.Vy = -60
        self.angle = 0

        self.mask = pg.mask.from_surface(self.image)

    def move(self, dt):
        """ Изменение координат и скоростей ракеты за время dt
        """
        ax = self.Fx / self.m
        ay = self.Fy / self.m
        self.rect.x += self.Vx * dt
        self.rect.y += self.Vy * dt
        self.Vx += ax * dt
        self.Vy += ay * dt

        if self.Vy == 0:
            if self.Vx > 0:
                self.angle = 90
            else:
                self.angle = -90
        else:
            t = -self.Vx / self.Vy
            if t > 0:
                self.angle = math.atan(t) / 2 / math.pi * 360 + 180
            else:
                self.angle = math.atan(t) / 2 / math.pi * 360

    def targetting(self, event):
        if event.pos[0] - self.rect.x > 0:
            self.angle = math.atan((self.rect.y - event.pos[1]) / (event.pos[0] - self.rect.x))
        elif event.pos[0] - self.rect.x < 0:
            self.angle = math.pi + math.atan((self.rect.y - event.pos[1]) / (event.pos[0] - self.rect.x))
        else:
            if self.rect.y - event.pos[1] >= 0:
                self.angle = math.pi / 2
            else:
                self.angle = -math.pi / 2


class Planet(pg.sprite.Sprite):
    def __init__(self, screen, x, y, filename):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.w = 100
        self.h = 100
        self.initial_image = pg.transform.scale(pg.image.load(filename).convert_alpha(), (self.w, self.h))
        self.image = self.initial_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.m = 10**16
        self.r = 50
        self.angle = 0
        self.omega = 1
        self.angle = 0

        self.mask = pg.mask.from_surface(self.image)
