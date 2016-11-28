# coding=utf-8


# region imports
import random
import numpy as np
import pygame
from numpy import array as vector

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

# endregion


# region class definition


# endregion


# region setup

screen = pygame.display.set_mode((WIDTH, HEIGHT))
done = False
clock = pygame.time.Clock()


# endregion


def main():
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
