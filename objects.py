import pygame as pg
import math
import random

class Rocket(pg.sprite.Sprite):
    def __init__(self, x, y, filename):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load(filename).convert_alpha(), (90, 90))
        self.rect = self.image.get_rect(center=(x, y))

        self.m = 10**5
        self.rect.x = x
        self.rect.y = y
        self.Fx = 0
        self.Fy = 0
        self.Vx = -20
        self.Vy = -50
        self.angle = 0

    def move(self, dt):
        ax = self.Fx / self.m
        ay = self.Fy / self.m
        self.rect.x += self.Vx * dt
        self.rect.y += self.Vy * dt
        self.Vx += ax * dt
        self.Vy += ay * dt
        if self.Vx / self.Vy < 0:
            self.angle = math.atan(-self.Vx / self.Vy) / 2 / math.pi * 360 + 180
        else:
            self.angle = math.atan(-self.Vx / self.Vy) / 2 / math.pi * 360

    def rotate(self):
        image = pg.transform.rotate(self.image, -self.angle)
        return image

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
