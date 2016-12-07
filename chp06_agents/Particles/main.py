# coding=utf-8


# region imports

from random import random, uniform

from numpy.linalg import norm
from numpy import array as vector
from numpy import dot
from math import acos, sin, cos

import pygame

from chp06_agents.Particles.FlowField import PerlinField3d

# from Vehicle import Vehicle

try:
    from Box2D import b2World
except ImportError:
    def b2World(*args, **kwargs):
        raise NotImplementedError()

from Particle import Mover
from Globals import WIDTH, HEIGHT, WHITE, mousepos, \
    is_mouse_down, norm, dist, normalize


# endregion

# region globals

def angle_between(vec1, vec2):
    product = dot(vec1, vec2)
    theta = acos(product / (norm(vec1) * norm(vec2)))
    return theta

# endregion


# region class definition

class Path:
    def __init__(self):
        self.points = []
        self.raduis = 20

    def add_point(self, x, y):
        self.points.append(vector((int(x), int(y))))

    def draw(self, scr):
        for i in range(len(self.points) - 1):
            start = self.points[i]
            end = self.points[i + 1]
            pygame.draw.line(scr, (255, 230, 255),
                             start, end,
                             self.raduis * 2)
            pygame.draw.circle(scr, (255, 230, 255),
                               start, self.raduis)
            pygame.draw.circle(scr, (255, 230, 255),
                               end, self.raduis)

        for i in range(len(self.points) - 1):
            start = self.points[i]
            end = self.points[i + 1]
            pygame.draw.line(scr, (255, 0, 255), start, end, 2)

    def get_normal(self, pos, predict_rate=50):
        best_normal = None
        best_dist = -1
        for i in range(len(self.points) - 1):
            start = self.points[i]
            end = self.points[i + 1]

            ab = normalize(end - start)
            ap = pos - start
            normal = ab * dot(ap, ab)  # + ab*predict_rate
            normal = start + normal
            future_normal = normal + ab * predict_rate

            to_end = end - future_normal
            from_start = future_normal - start
            if dot(to_end, from_start) < 0:
                normal = end

            d = dist(normal, pos)
            if best_dist == -1 or d < best_dist:
                best_dist = d
                best_normal = future_normal
        if best_normal is not None:
            return best_normal


class Vehicle(Mover):
    def __init__(self, pos):
        super().__init__(pos)
        self.maxspeed = 4
        self.maxforce = 0.3
        self.desired = vector((0, 0))
        self.theta = 0
        self.velocity = vector([uniform(-self.maxspeed / 2, self.maxspeed / 2),
                                uniform(-self.maxspeed / 2, self.maxspeed / 2)])

    def draw(self, scr, debug=False):
        pos = (int(self.position[0]), int(self.position[1]))
        pygame.draw.circle(scr, (0, 0, 0), pos, 5, 1)
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

    def track(self, path, scr=None, debug=False):
        prediction_rate = 25
        future_loc = self.position + normalize(self.velocity) * prediction_rate
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

# endregion


# region setup

screen = pygame.display.set_mode((WIDTH, HEIGHT))
done = False
clock = pygame.time.Clock()

show_velocities = False
show_field = False
show_path = True

movers = []
movers.append(Vehicle((WIDTH / 2, HEIGHT / 2)))

flowfiled = PerlinField3d()

path = Path()
path.add_point(100, 100)
path.add_point(WIDTH - 100, 100)
path.add_point(WIDTH - 100, HEIGHT - 100)
path.add_point(WIDTH / 2, HEIGHT - 250)
path.add_point(100, HEIGHT - 100)
path.add_point(100, 100)

# endregion


def main():
    screen.fill(WHITE)

    if is_mouse_down and random() < 0.8:
        movers.append(Vehicle(mousepos.copy()))

    if show_path:
        path.draw(screen)

    if show_field:
        flowfiled.draw(screen)
    # flowfiled.update()

    for particle in movers:
        particle.run(screen, show_velocities)
        # particle.follow(flowfiled)
        particle.track(path, screen, show_velocities)

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
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            show_velocities = not show_velocities
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            show_field = not show_field
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            show_path = not show_path
    main()
