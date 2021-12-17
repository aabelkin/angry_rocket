import pygame as pg
import math
import random


class Rocket(pg.sprite.Sprite):
    """Класс Rocket

    Атрибуты
    ----------
    screen : pygame.Surface
        экран, на котором будет нарисована ракета
    w, h : int
        ширина и высота ракеты
    image : pygame.Surface
        поверхность с изображением ракеты размером w на h
    rect : pygame.Rect
        прямоугольник, огибающий изображение ракеты
    Fx, Fy : float
        проекции сил, действующих на ракету по осям x и y
    Vx, Vy : float
        проекции скоростей ракеты на оси x и y
    angle : float
        угол поворота ракеты относительно вертикали против часовой стрелки
    mask : pygame.mask.Mask
        маска ракеты (требуется для проверки столкновений с другими объектами)
    """

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
        """Изменяет координаты ракеты, ее скорость и угол поворота
        за время dt действия сил со стороны других объектов

        Параметры
        ----------
        dt : float
            время действия сил
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
    """Класс Planet

    Атрибуты
    ----------
    screen : pygame.Surface
        экран, на котором будет нарисована планета
    r : int
        радиус планеты
    w, h : int
        ширина и высота планеты, задаваемые ее радиусом
    image : pygame.Surface
        поверхность с изображением планеты размером w на h
    rect : pygame.Rect
        прямоугольник, огибающий изображение планеты
    m : float
        масса планеты
    period : float
        период обращения планеты вокруг своей оси
    direction : int
        направление вращения планеты (1, если против часовой стрелки, иначе -1)
    angle : float
        угол поворота планеты относительно вертикали против часовой стрелки
    mask : pygame.mask.Mask
        маска планеты (требуется для проверки столкновений с другими объектами)
    """

    def __init__(self, screen, x, y, r, direction):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.r = r
        self.w = 2 * r
        self.h = 2 * r
        rand_image = 'images/planets/' + str(random.randint(1, 5)) + '.png'
        self.initial_image = pg.transform.scale(pg.image.load(rand_image).convert_alpha(), (self.w, self.h))
        self.image = self.initial_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.m = 10**16 * r
        self.period = 5
        self.direction = direction
        self.angle = 0

        self.mask = pg.mask.from_surface(self.image)


class Comet(pg.sprite.Sprite):
    """Класс Comet

    Атрибуты
    ----------
    screen : pygame.Surface
        экран, на котором будет нарисована комета
    r : int
        радиус кометы
    w, h : int
        ширина и высота кометы, задаваемые ее радиусом
    image : pygame.Surface
        поверхность с изображением кометы размером w на h
    rect : pygame.Rect
        прямоугольник, огибающий изображение кометы
    m : float
        масса кометы
    mask : pygame.mask.Mask
        маска кометы (требуется для проверки столкновений с ракетой)
    """
    def __init__(self, screen, x, y, r, filename):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.r = r
        self.w = 2 * r
        self.h = 2 * r
        self.image = pg.transform.scale(pg.image.load(filename).convert_alpha(), (self.w, self.h))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.m = 5 * 10**14 * r

        self.mask = pg.mask.from_surface(self.image)


class Background(pg.sprite.Sprite):
    """Класс Background - фон игры

    Атрибуты
    ----------
    w, h : int
        ширина и высота фона
    image : pygame.Surface
        поверхность с изображением фона игры размером w на h
    rect : pygame.Rect
        прямоугольник, огибающий изображение фона
    """
    def __init__(self, w, h, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load('images/background.jpg').convert_alpha(), (w, h))
        self.rect = self.image.get_rect()
        self.rect.center = (w / 2, y)
