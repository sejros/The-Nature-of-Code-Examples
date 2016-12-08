from math import sin, cos
from random import uniform, random

import pygame
from numpy import array as vector
from numpy.linalg import norm

from Particle import Mover
from Globals import normalize, dist, WIDTH, HEIGHT


class Vehicle(Mover):
    def __init__(self, pos, size=5, speed=5):
        super().__init__(pos)
        self.size = size
        self.maxspeed = speed
        self.maxforce = self.maxspeed / 5
        self.desired = vector((0, 0))
        self.theta = 0
        self.velocity = vector([uniform(-self.maxspeed / 2, self.maxspeed / 2),
                                uniform(-self.maxspeed / 2, self.maxspeed / 2)])

    def draw(self, scr, debug=False):
        pos = (int(self.position[0]), int(self.position[1]))
        pygame.draw.circle(scr, (0, 0, 0), pos, self.size, 1)
        if debug:
            scale = 5
            end = (int(pos[0] + self.velocity[0] * scale),
                   int(pos[1] + self.velocity[1] * scale))
            pygame.draw.line(scr, (200, 0, 0), pos, end, 2)

            end = (int(pos[0] + self.desired[0] * scale),
                   int(pos[1] + self.desired[1] * scale))
            pygame.draw.line(scr, (0, 200, 0), pos, end, 2)

    def steer(self, desired):
        # steer = vector((0, 1))

        if norm(desired) > self.maxspeed:
            desired = normalize(desired) * self.maxspeed
        self.desired = desired
        steer = desired - self.velocity
        steer = normalize(steer) * self.maxforce
        # steer.normalize()


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
        # desired = field.lookup(self.position + self.velocity)
        desired = field.lookup(self.position)
        self.steer(desired)

    def track(self, path, scr=None, debug=False):
        prediction_rate = 25
        future_loc = self.position + normalize(self.velocity) * prediction_rate
        # future_loc = vector((0, 1))
        normal_loc = path.get_normal(future_loc)

        if debug:
            pygame.draw.circle(scr, (255, 128, 255),
                               (int(normal_loc[0]), int(normal_loc[1])), 10)
            pygame.draw.circle(scr, (255, 230, 255),
                               (int(future_loc[0]), int(future_loc[1])), 10)

        if dist(future_loc, normal_loc) > path.raduis:
            self.seek(normal_loc)

    def run(self, scr, debug):
        self.update()

        self.toroid()
        # self.wander()
        # self.bounce()

        self.draw(scr, debug)
