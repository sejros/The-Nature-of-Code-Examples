# coding=utf-8


# region imports

from math import acos
from random import random, uniform

import pygame
from numpy import array as vector
from numpy import dot
from numpy.linalg import norm

from chp06_agents.Particles.FlowField import PathField, Grid
from chp06_agents.Particles.Path import Path

try:
    from Box2D import b2World
except ImportError:
    def b2World(*args, **kwargs):
        raise NotImplementedError()

from Vehicle import Vehicle
from Globals import WIDTH, HEIGHT, WHITE, mousepos, \
    is_mouse_down, norm


# endregion

# region globals

def angle_between(vec1, vec2):
    product = dot(vec1, vec2)
    theta = acos(product / (norm(vec1) * norm(vec2)))
    return theta

# endregion


# region class definition



# endregion


# region setup

screen = pygame.display.set_mode((WIDTH, HEIGHT))
done = False
clock = pygame.time.Clock()
old_time = pygame.time.get_ticks()
frames, total_waited = 0, 0

show_velocities = False
show_field = False
show_path = False
show_grid = False

# movers = []
movers = Grid(resolution=15)

N = 100
for i in range(N):
    movers.append(Vehicle(vector((uniform(0, WIDTH), uniform(0, HEIGHT))),
                          size=5, speed=10))

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
    if show_grid:
        movers.draw(screen)
    movers.update()

    for particle in movers:
        particle.update()
        particle.toroid()
        # particle.bounce()
        particle.draw(screen, show_velocities)
        # particle.seek(mousepos)

        # particle.separate(movers)
        particle.separate(movers.nearest(particle.position, radius=15))
        particle.cohese(movers.nearest(particle.position, radius=15))
        particle.align(movers.nearest(particle.position, radius=15))

        # particle.follow(flowfiled)
        # particle.track(path, screen, show_velocities)
        # pass

    # x = movers[0]
    # near = movers.nearest(x.position, radius=15)
    # for x_ in near:
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
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            show_grid = not show_grid
    main()

print(total_waited * 1000 / frames / N)
