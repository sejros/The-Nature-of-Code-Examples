# coding=utf-8

import random
from math import pi

import pygame
from Box2D import b2PolygonShape, b2CircleShape
from .Globals import WIDTH, HEIGHT

scale_factor = 10.0
transX = WIDTH / 2
transY = HEIGHT / 2


def vec_pixels2world(vec2):
    x, y = vec2[0], vec2[1]
    x_ = (x - transX) / scale_factor
    y_ = (transY - y) / scale_factor
    return x_, y_


def vec_world2pixels(vec2):
    x, y = vec2[0], vec2[1]
    x_ = x * scale_factor + transX
    y_ = (1 - y) * scale_factor + transY
    return x_, y_


def scalar_pixels2world(val):
    return val / scale_factor


def scalar_world2pixels(val):
    return val * scale_factor


class Particle:
    def __init__(self, world, pos, circle=False, size=None):
        pos = vec_pixels2world(pos)
        if size:
            self.size = size
        else:
            self.size = (random.random() * 10 + 5, random.random() * 10 + 5)

        if circle:
            shape = b2CircleShape(pos=(pos[0], pos[1]), radius=size)
        else:
            shape = b2PolygonShape(box=(scalar_pixels2world(self.size[0] / 2),
                                        scalar_pixels2world(self.size[1] / 2)))

        self.body = world.CreateDynamicBody(position=(pos[0], pos[1]),
                                            shapes=shape)
        self.box = self.body.CreateCircleFixture(shape=shape, density=1.0, friction=0.3)

        self.lifespan = 150
        self.life = self.lifespan

    def draw(self, scr):
        s = pygame.Surface(self.size, pygame.SRCALPHA)  # per-pixel alpha
        s.fill((127, 127, 127, int((255.0 / self.lifespan) * self.life)))  # notice the alpha value in the color
        pygame.draw.rect(s, (0, 0, 0, int((255.0 / self.lifespan) * self.life)),
                         [0, 0,
                          self.size[0], self.size[1]], 3)
        s = pygame.transform.rotate(s, self.body.angle * 180 / pi)

        pos = vec_world2pixels(self.body.position)
        pos = (pos[0] - self.size[0] / 2, pos[1] - self.size[1] / 2)
        scr.blit(s, pos)

    def delete(self, world):
        world.DestroyBody(self.body)
        pass
