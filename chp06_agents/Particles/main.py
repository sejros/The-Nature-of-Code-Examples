# coding=utf-8


# region imports

from random import random

import pygame

from chp06_agents.Particles.FlowField import PerlinField3d
from Vehicle import Vehicle

try:
    from Box2D import b2World
except ImportError:
    def b2World(*args, **kwargs):
        raise NotImplementedError()

from Globals import WIDTH, HEIGHT, WHITE, mousepos, is_mouse_down

# endregion


# region globals

# endregion


# region class definition


# endregion


# region setup

screen = pygame.display.set_mode((WIDTH, HEIGHT))
done = False
clock = pygame.time.Clock()

debug = False
Show_Flow = False

movers = []
movers.append(Vehicle((WIDTH / 2, HEIGHT / 2)))

flowfiled = PerlinField3d()

# endregion


def main():
    screen.fill(WHITE)

    if is_mouse_down and random() < 0.8:
        movers.append(Vehicle(mousepos.copy()))

    for particle in movers:
        particle.run(screen, debug)
        particle.follow(flowfiled)

    if Show_Flow:
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
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            debug = not debug
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            Show_Flow = not Show_Flow
    main()
