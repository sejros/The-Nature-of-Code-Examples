# coding=utf-8


# region imports

from math import acos, sin, cos, sqrt
from random import random, uniform

import pygame
from numpy import array as vector
from numpy import dot
from numpy.linalg import norm

from chp06_agents.Particles.FlowField import PathField
from chp06_agents.Particles.Path import Path

try:
    from Box2D import b2World
except ImportError:
    def b2World(*args, **kwargs):
        raise NotImplementedError()

from Particle import Mover
from Vehicle import Vehicle as BaseVehicle
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

class Vehicle(BaseVehicle):
    def separate(self, vehicles, radius=20, debug=False):
        radius = self.size * 2
        sum_vel = vector((0.0, 0.0))
        n = 0
        for other in vehicles:
            d = dist(self.position, other.position)
            if 0 < d < radius:
                n += 1
                diff = normalize(self.position - other.position) / d
                sum_vel += diff
        if n > 0:
            sum_vel /= n
            sum_vel = normalize(sum_vel) * self.maxspeed
            self.steer(sum_vel)

    def cohese(self, vehicles, radius=20, debug=False):
        radius = self.size * 2
        sum_vel = vector((0.0, 0.0))
        n = 0
        for other in vehicles:
            d = dist(other.position, self.position)
            if d > radius:
                n += 1
                diff = normalize(other.position - self.position)
                sum_vel += diff
        if n > 0:
            sum_vel /= n
            sum_vel = normalize(sum_vel) * self.maxspeed
            self.steer(sum_vel)


class Grid:
    def __init__(self, resolution=40):
        self.resolution = resolution
        self.cols = int(WIDTH / self.resolution)
        self.rows = int(HEIGHT / self.resolution)
        self.objects = []
        self._init()

    def __iter__(self):
        return iter(self.objects)

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, index):
        return self.objects[index]

    def _init(self):
        self.grid = []
        for i in range(self.cols):
            row = []
            for j in range(self.rows):
                row.append([])
            self.grid.append(row)

    def append(self, obj):
        self.objects.append(obj)
        self._add_object(obj)

    def _add_object(self, obj):
        col = int(obj.position[0] / self.resolution) % self.cols - 1
        row = int(obj.position[1] / self.resolution) % self.rows - 1
        (self.grid[col][row]).append(obj)

    def update(self):
        self._init()
        for obj in self.objects:
            self._add_object(obj)

    def nearest(self, pos):
        col = int(pos[0] / self.resolution) % self.cols - 1
        row = int(pos[1] / self.resolution) % self.rows - 1

        res = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                res.extend(self.grid[col + i][row + j])

        return res


# endregion


# region setup

screen = pygame.display.set_mode((WIDTH, HEIGHT))
done = False
clock = pygame.time.Clock()
old_time = pygame.time.get_ticks()
frames, total_waited = 0, 0

show_velocities = False
show_field = False
show_path = True

# movers = []
movers = Grid()

N = 100
for i in range(N - 1):
    movers.append(Vehicle(vector((uniform(0, WIDTH), uniform(0, HEIGHT))),
                          size=10, speed=10))

path = Path()
path.add_point(100, 100)
path.add_point(WIDTH - 100, 100)
path.add_point(WIDTH - 100, HEIGHT - 100)
path.add_point(WIDTH / 2, HEIGHT - 150)
path.add_point(100, HEIGHT - 100)
path.add_point(100, 100)

flowfiled = PathField(path)

# endregion


def main():
    global old_time, frames, total_waited
    screen.fill(WHITE)
    if is_mouse_down and random() < 0.8:
        movers.append(Vehicle(mousepos.copy(), size=10))
    if show_path:
        path.draw(screen)
    if show_field:
        flowfiled.draw(screen)
    # flowfiled.update()
    movers.update()

    for particle in movers:
        particle.update()
        particle.toroid()
        # particle.bounce()
        particle.draw(screen, show_velocities)
        # particle.seek(mousepos)

        # particle.separate(movers)
        particle.separate(movers.nearest(particle.position))
        particle.cohese(movers.nearest(particle.position))

        # particle.follow(flowfiled)
        # particle.track(path, screen, show_velocities)
        pass

    # x = movers[0]
    # for x_ in movers.nearest(x.position):
    #     pygame.draw.circle(screen, (255, 0, 0),
    #                        (int(x_.position[0]), int(x_.position[1])),
    #                        x.size, 3)
    # pygame.draw.circle(screen, (0, 255, 0),
    #                    (int(x.position[0]), int(x.position[1])),
    #                    x.size, 3)

    # print(len(movers))

    pygame.display.flip()

    pygame.time.wait(0)
    new_time = pygame.time.get_ticks()
    waited = new_time - old_time
    old_time = new_time
    frames += 1
    total_waited += waited

    clock.tick(30)


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

print(total_waited * 100 / frames / N)
