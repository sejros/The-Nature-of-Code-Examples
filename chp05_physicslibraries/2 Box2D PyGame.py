# coding=utf-8


# region imports
import random
import numpy as np
import pygame
from numpy import array as vector
from math import pi

from Box2D import b2PolygonShape, b2World, b2CircleShape

# endregion


# region globals

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

mousepos = vector([WIDTH / 2, HEIGHT / 2])
is_mouse_down = False
is_rmouse_down = False

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


# endregion


# region class definition

class Particle:
    def __init__(self, world, pos, size=None):
        pos = vec_pixels2world(pos)
        if size:
            self.size = size
        else:
            self.size = (random.random() * 10 + 5, random.random() * 10 + 5)

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


class ParticleSystem:
    def __init__(self, world, pos):
        self.pos = pos
        self.world = world
        self.particles = []

    def draw(self, c):
        for particle in self.particles:
            particle.draw(c)

    def update(self):
        if random.random() < 0.5:
            self.particles.append(Particle(self.world, self.pos.copy()))

        for particle in self.particles:
            particle.life -= 1
            if particle.life <= 0:
                particle.delete(self.world)
                self.particles.remove(particle)

    def run(self, c):
        self.update()
        self.draw(c)


# endregion


# region setup

screen = pygame.display.set_mode((WIDTH, HEIGHT))
done = False
clock = pygame.time.Clock()

world = b2World(gravity=(0, -10))
# Box2D.listenForCollisions()

# part = Particle(world, (WIDTH/2, HEIGHT / 2), size=(50, 50))
# part2 = Particle(world, (WIDTH/2 + 100, HEIGHT / 2), size=(20, 20))

pss = []


# endregion


def main():
    screen.fill(WHITE)
    world.Step(1.0 / 60, 6, 2)

    # if is_mouse_down:
    #     part2.body.position = vec_pixels2world(mousepos)
    #
    # part.draw(screen)
    # part2.draw(screen)

    for system in pss:
        system.run(screen)

    pygame.display.flip()
    clock.tick(60)


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEMOTION:
            mousepos = [event.pos[0], event.pos[1]]
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            is_mouse_down = True
            pss.append(ParticleSystem(world, mousepos))
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            is_mouse_down = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            is_rmouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            is_rmouse_down = False
    main()
