# coding=utf-8


# region imports

from random import random
from numpy import array as vector
from numpy.linalg import norm

import pygame

try:
    from Box2D import b2World
except ImportError:
    def b2World(*args, **kwargs):
        raise NotImplementedError()

from Particle import Mover

from Globals import WIDTH, HEIGHT, WHITE, mousepos, is_mouse_down, normalize, dist

# endregion


# region globals

# endregion


# region class definition

class Vehicle(Mover):
    def __init__(self, pos):
        super().__init__(pos)
        self.maxspeed = 4
        self.maxforce = 0.05
        self.desired = vector((0, 0))

    def draw(self, scr, debug=False):
        pos = (int(self.position[0]), int(self.position[1]))
        pygame.draw.circle(scr, (0, 0, 0), pos, 10, 1)
        if debug:
            scale = 5
            end = (int(pos[0] + self.velocity[0] * scale),
                   int(pos[1] + self.velocity[1] * scale))
            pygame.draw.line(scr, (200, 0, 0), pos, end, 2)

            end = (int(pos[0] + self.desired[0] * scale),
                   int(pos[1] + self.desired[1] * scale))
            pygame.draw.line(scr, (0, 200, 0), pos, end, 2)

    def run(self, scr):
        self.update()
        self.toroid()
        self.arrive2(mousepos)
        self.draw(scr, True)

    def steer(self, desired):
        if norm(desired) > self.maxspeed:
            desired = normalize(desired) * self.maxspeed
        self.desired = desired
        steer = desired - self.velocity
        steer = normalize(steer) * self.maxforce

        self.apply(steer)

    def seek(self, target):
        self.steer(target - self.position)

    def flee(self, target):
        self.steer(self.position - target)

    def arrive(self, target):
        self.steer((target - self.position) * 0.1)

    def arrive2(self, target, radius=200):
        desired = target - self.position
        d = dist(self.position, target)
        if d < radius:
            desired = desired * d / radius
        self.steer(desired)

    def wander(self):
        pass


# endregion


# region setup

screen = pygame.display.set_mode((WIDTH, HEIGHT))
done = False
clock = pygame.time.Clock()

movers = []

movers.append(Vehicle((WIDTH / 2, HEIGHT / 2)))

# endregion


def main():
    screen.fill(WHITE)

    if is_mouse_down and random() < 0.8:
        movers.append(Vehicle(mousepos.copy()))

    for particle in movers:
        particle.run(screen)

    print(len(movers))

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
            # pss.append(ParticleSystem(box2d_world, mousepos))
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            is_mouse_down = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            is_rmouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            is_rmouse_down = False
    main()
