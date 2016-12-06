# coding=utf-8


# region imports

from random import random, uniform
from numpy import array as vector
from numpy.linalg import norm
from math import pi, sin, cos
from noise import pnoise2, pnoise3

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

class FlowField:
    def __init__(self):
        self.field = []
        self.resolution = 20
        self.cols = int(WIDTH / self.resolution)
        self.rows = int(HEIGHT / self.resolution)
        for i in range(self.cols):
            row = []
            for j in range(self.rows):
                row.append(vector((10, 0)))
            self.field.append(row)

    def lookup(self, location):
        col = int(location[0] / self.resolution) % self.cols - 1
        row = int(location[1] / self.resolution) % self.cols - 1
        return self.field[col][row]

    def draw(self, scr):
        for i in range(self.cols):
            for j in range(self.rows):
                center = vector((int((i + 0.5) * self.resolution),
                                 int((j + 0.5) * self.resolution)))
                pygame.draw.circle(scr, (255, 255, 0), center,
                                   int(self.resolution / 5), 1)
                pygame.draw.line(scr, (255, 255, 0),
                                 center, center + self.field[i][j], 1)


class PerlinField(FlowField):
    def __init__(self):
        super().__init__()
        delta = 0.05
        xoff, yoff = 0, 0
        for i in range(self.cols):
            yoff = 0
            for j in range(self.rows):
                angle = pnoise2(xoff, yoff) * 2 * pi
                self.field[i][j] = vector((sin(angle), cos(angle))) * 10
                yoff += delta
            xoff += delta


class PerlinField3d(FlowField):
    def __init__(self):
        super().__init__()
        self.toff = 0
        self.generate()

    def update(self):
        self.toff += 0.01
        self.generate()

    def generate(self):
        delta = 0.05
        xoff, yoff = 0, 0
        for i in range(self.cols):
            yoff = 0
            for j in range(self.rows):
                angle = pnoise3(xoff, yoff, self.toff) * 2 * pi
                self.field[i][j] = vector((sin(angle), cos(angle))) * 20
                yoff += delta
            xoff += delta


class Vehicle(Mover):
    def __init__(self, pos):
        super().__init__(pos)
        self.maxspeed = 10
        self.maxforce = 0.5
        self.desired = vector((0, 0))
        self.theta = 0
        self.velocity = vector([uniform(-self.maxspeed / 2, self.maxspeed / 2),
                                uniform(-self.maxspeed / 2, self.maxspeed / 2)])

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

    def wander(self, d=50, r=25, change=0.5):
        center = normalize(self.velocity) * d + self.position
        self.theta += random() * 2 * change - change
        randrad = vector((sin(self.theta), cos(self.theta))) * r
        desired = center + randrad

        self.steer(desired - self.position)

    def bounce(self, d=50):
        if d > self.position[0]:
            self.steer(vector((self.maxspeed, self.velocity[1])))
        if self.position[0] > WIDTH - d:
            self.steer(vector((-self.maxspeed, self.velocity[1])))
        if d > self.position[1]:
            self.steer(vector((self.velocity[1], self.maxspeed)))
        if self.position[1] > HEIGHT - d:
            self.steer(vector((self.velocity[1], -self.maxspeed)))

    def follow(self, field):
        desired = field.lookup(self.position + self.velocity)
        self.steer(desired)

    def run(self, scr):
        self.update()

        self.toroid()
        # self.wander()
        # self.bounce()

        self.draw(scr, True)


# endregion


# region setup

screen = pygame.display.set_mode((WIDTH, HEIGHT))
done = False
clock = pygame.time.Clock()

movers = []
movers.append(Vehicle((WIDTH / 2, HEIGHT / 2)))

flowfiled = PerlinField3d()

# endregion


def main():
    screen.fill(WHITE)

    if is_mouse_down and random() < 0.8:
        movers.append(Vehicle(mousepos.copy()))

    for particle in movers:
        particle.run(screen)
        particle.follow(flowfiled)

    flowfiled.draw(screen)
    flowfiled.update()

    # print(len(movers))

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
