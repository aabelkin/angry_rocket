import pygame as pg
import math
from vis import *
import random

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
        self.Vx = -40
        self.Vy = -70
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
                self.angle = -90
            else:
                self.angle = 90
        else:
            t = -self.Vx / self.Vy
            if t > 0:
                if self.Vx > 0:
                    self.angle = -math.degrees(math.atan(t))
                else:
                    self.angle = 180 - math.degrees(math.atan(t))
            else:
                if self.Vx < 0:
                    self.angle = math.degrees(math.atan(-t))
                else:
                    self.angle = math.degrees(math.atan(-t)) - 180


class Planet(pg.sprite.Sprite):
    def __init__(self, screen, x, y, r, direction, filename):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.r = r
        self.w = 2 * r
        self.h = 2 * r
        self.initial_image = pg.transform.scale(pg.image.load(filename).convert_alpha(), (self.w, self.h))
        self.image = self.initial_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.m = 10**16 * r
        self.period = 5
        self.direction = direction
        self.angle = 0

        self.mask = pg.mask.from_surface(self.image)


class Comet(pg.sprite.Sprite):
    def __init__(self, screen, x, y, Vx, Vy, filename):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.w = 30
        self.h = 30
        self.initial_image = pg.transform.scale(pg.image.load(filename).convert_alpha(), (self.w, self.h))
        self.image = self.initial_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.rect.x = x
        self.rect.y = y
        self.Vx = Vx
        self.Vy = Vy
        self.angle = 0

        self.mask = pg.mask.from_surface(self.image)

    def move(self, dt):
        """ Изменение координат и скоростей ракеты за время dt
        """
        self.rect.x += self.Vx * dt
        self.rect.y += self.Vy * dt
