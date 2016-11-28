# coding=utf-8

from tkinter import *
import numpy as np
from numpy import array as vector
from numpy.linalg import norm as normalize
import random
from math import sqrt, sin, cos

from Box2D import (b2PolygonShape, b2World, b2CircleShape)

WIDTH = 800
HEIGHT = 600

mousepos = np.array([WIDTH / 2, HEIGHT / 2])
is_mouse_down = False
is_rmouse_down = False

scale_factor = 20.0
transX = WIDTH / 2
transY = HEIGHT / 2


def pixels2world(vec2):
    x, y = vec2[0], vec2[1]
    x_ = (x - transX) / scale_factor
    y_ = (transY - y) / scale_factor
    return x_, y_


def world2pixels(vec2):
    x, y = vec2[0], vec2[1]
    x_ = x * scale_factor + transX
    y_ = (1 - y) * scale_factor + transY
    return x_, y_


def mousemove(event):
    global mousepos
    mousepos = np.array([float(event.x), float(event.y)])


def mousedown(event):
    global is_mouse_down
    is_mouse_down = True
    pss.append(ParticleSystem(world, mousepos))


def mouseup(event):
    global is_mouse_down
    is_mouse_down = False


def rmousedown(event):
    global is_rmouse_down
    is_rmouse_down = True


def rmouseup(event):
    global is_rmouse_down
    is_rmouse_down = False


class Particle:
    def __init__(self, world, pos, size=(16, 16), radius=10):
        pos = pixels2world(pos)

        shape = b2CircleShape(pos=(pos[0], pos[1]), radius=radius)
        self.body = world.CreateDynamicBody(position=(pos[0], pos[1]),
                                            shapes=shape)
        self.box = self.body.CreateCircleFixture(shape=shape, density=1.0, friction=0.3)

        self.lifespan = 60
        self.size = size
        self.radius = radius
        self.mover = None

    def draw(self, canvas):
        canvas.delete(self.mover)

        pos = world2pixels(self.body.position)
        self.mover = canvas.create_oval(pos[0] - self.radius / 2,
                                        pos[1] - self.radius / 2,
                                        pos[0] + self.radius / 2,
                                        pos[1] + self.radius / 2,
                                        fill="Red")


class ParticleSystem:
    def __init__(self, world, pos):
        self.pos = pos
        self.world = world
        self.particles = []

    def draw(self, c):
        for particle in self.particles:
            particle.draw(c)

    def update(self, c):
        self.particles.append(Particle(self.world, self.pos.copy()))

        for particle in self.particles:
            if particle.lifespan <= 0:
                c.delete(particle.mover)
                self.particles.remove(particle)

    def run(self, c):
        self.update(c)
        self.draw(c)


root = Tk()
root.title("Tkinter demo")
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#ffffff")
c.pack()
c.bind('<Motion>', mousemove)
c.bind('<Button-1>', mousedown)
c.bind('<ButtonRelease-1>', mouseup)
c.bind('<Button-2>', rmousedown)
c.bind('<ButtonRelease-3>', rmouseup)

world = b2World(gravity=(0, -10))

part = Particle(world, (WIDTH / 2, HEIGHT / 2))

pss = []


def main():
    world.Step(1.0 / 60, 6, 2)

    # part.draw(c)

    # print(part.body.position, world2pixels(part.body.position))

    for system in pss:
        system.run(c)

    root.after(25, main)  # 40 fps


# bob = Mover(np.array([WIDTH/2, 300]))
# spring = Spring(origin=np.array([WIDTH/2, 0]), rest=200)
# spring.attach(bob)

main()
root.mainloop()
