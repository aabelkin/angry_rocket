import pygame as pg
import math
import random

class Rocket(pg.sprite.Sprite):
    def __init__(self, screen, x, y, filename):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.w = 60
        self.h = 60
        self.image = pg.transform.scale(pg.image.load(filename).convert_alpha(), (self.w, self.h))
        self.rect = self.image.get_rect(center=(x, y))

        self.m = 10**5
        self.rect.x = x
        self.rect.y = y
        self.Fx = 0
        self.Fy = 0
        self.Vx = -15
        self.Vy = -35
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

    def flight_rotation(self):
        """ Поворот ракеты в сторону вектора скорости при движении
        """
        if self.Vx / self.Vy < 0:
            self.angle = math.atan(-self.Vx / self.Vy) / 2 / math.pi * 360 + 180
        else:
            self.angle = math.atan(-self.Vx / self.Vy) / 2 / math.pi * 360

    def draw(self):
        """ Рисование ракеты
        """
        image = pg.transform.rotate(self.image, -self.angle)
        self.screen.blit(image, (self.rect.x, self.rect.y))

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
    def __init__(self, x, y, filename):
        pg.sprite.Sprite.__init__(self)
        image = pg.image.load(filename).convert_alpha()
        self.image = pg.transform.scale(image, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))

        self.m = 10**16
        self.x = x
        self.y = y
        self.r = 50

        self.mask = pg.mask.from_surface(self.image)
