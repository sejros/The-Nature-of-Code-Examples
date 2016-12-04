# coding=utf-8

import random
from abc import abstractmethod, ABCMeta
from math import pi

import pygame
from Box2D import b2PolygonShape, b2CircleShape

from chp05_physicslibraries.Particles.Globals import vec_pixels2world, vec_world2pixels, scalar_pixels2world


class Sprite(metaclass=ABCMeta):
    def __init__(self):
        self.lifespan = 150
        self.size = (random.random() * 10 + 5, random.random() * 10 + 5)

    @abstractmethod
    def draw(self, scr):
        pass

    @abstractmethod
    def delete(self, world):
        pass


# TODO from chapter 4 and 3

class Particle(Sprite):
    def __init__(self, world, pos, circle=False, size=None):
        super().__init__()
        pos = vec_pixels2world(pos)
        if size:
            self.size = size
        else:
            pass

        if circle:
            shape = b2CircleShape(pos=(pos[0], pos[1]), radius=size)
        else:
            shape = b2PolygonShape(box=(scalar_pixels2world(self.size[0] / 2),
                                        scalar_pixels2world(self.size[1] / 2)))

        self.body = world.CreateDynamicBody(position=(pos[0], pos[1]),
                                            shapes=shape)
        self.box = self.body.CreateCircleFixture(shape=shape, density=1.0, friction=0.3)

        self.life = self.lifespan

        self.pos = self.body.position

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
