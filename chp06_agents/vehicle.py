# coding=utf-8


# region imports

import pygame
from Box2D import b2World

from Particles import Particle, WIDTH, HEIGHT, WHITE, mousepos, is_mouse_down


# endregion


# region globals

# endregion


# region class definition

class Vehicle(Particle):
    pass


# endregion


# region setup

screen = pygame.display.set_mode((WIDTH, HEIGHT))
done = False
clock = pygame.time.Clock()

box2d_world = b2World(gravity=(0, 0))

pss = []


# endregion


def main():
    screen.fill(WHITE)
    box2d_world.Step(1.0 / 60, 6, 2)

    if is_mouse_down:
        pss.append(Vehicle(box2d_world, mousepos.copy()))

    for particle in pss:
        particle.draw(screen)

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
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            is_mouse_down = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            is_rmouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            is_rmouse_down = False
    main()
