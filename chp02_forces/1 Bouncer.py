# coding=utf-8

import random
from tkinter import *

import numpy as np

WIDTH = 800
HEIGHT = 600

mousepos = np.array([WIDTH / 2, HEIGHT / 2])
is_mouse_down = False
is_rmouse_down = False


class Liquid:
    def __init__(self):
        self.density = 0.5

    def draw(self, canvas):
        canvas.create_rectangle(0, HEIGHT/2, WIDTH, HEIGHT,
                                fill="grey"+str(int(100-self.density*100)))

    def contains(self, obj):
        return obj.position[1] > HEIGHT/2


class Mover:
    def __init__(self):
        # self.position = np.array([WIDTH / 2.0, HEIGHT / 2.0])
        self.position = np.array([random.randint(0, WIDTH), HEIGHT / 8.0])
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.mover = None
        # self.mass = 1.0
        self.mass = random.uniform(0.5, 2.0)
        self.BALL_RADIUS = 20 * self.mass

    def apply(self, force):
        self.acceleration += force / self.mass

    def update(self, trail=False):

        self.velocity += self.acceleration

        if trail:
            c.create_line(self.position[0], self.position[1],
                          self.position[0] + self.velocity[0],
                          self.position[1] + self.velocity[1],
                          width=self.BALL_RADIUS / 4, fill="red")

        self.position += self.velocity

        self.acceleration = np.array([0.0, 0.0])

        self.bounce()

    def draw(self, canvas):
        canvas.delete(self.mover)
        self.mover = canvas.create_oval(self.position[0] - self.BALL_RADIUS / 2,
                                        self.position[1] - self.BALL_RADIUS / 2,
                                        self.position[0] + self.BALL_RADIUS / 2,
                                        self.position[1] + self.BALL_RADIUS / 2,
                                        fill="Red")

    def bounce(self):
        if 0 > self.position[0]:
            self.position[0] = 0
            self.velocity[0] *= -1
        if self.position[0] > WIDTH:
            self.position[0] = WIDTH
            self.velocity[0] *= -1
        if 0 > self.position[1]:
            self.position[1] = 0
            self.velocity[1] *= -1
        if self.position[1] > HEIGHT:
            self.position[1] = HEIGHT
            self.velocity[1] *= -1

    def toroid(self):
        self.position[0] %= WIDTH
        self.position[1] %= HEIGHT


def mousemove(event):
    global mousepos
    mousepos = np.array([event.x, event.y])


def mousedown(event):
    global is_mouse_down
    is_mouse_down = True


def mouseup(event):
    global is_mouse_down
    is_mouse_down = False


def rmousedown(event):
    global is_rmouse_down
    is_rmouse_down = True


def rmouseup(event):
    global is_rmouse_down
    is_rmouse_down = False


def main():

    liquid.draw(c)

    for mover in movers:
        gravity = np.array([0, 0.2]) * mover.mass
        mover.apply(gravity)

        wind = np.array([0.2, 0])
        if is_mouse_down:
            mover.apply(wind)

        # friction_coeff = -0.1
        # friction = friction_coeff * mover.velocity
        # mover.apply(friction)

        # drag_coeff = -0.05
        # drag = drag_coeff * mover.velocity * np.linalg.norm(mover.velocity)
        # mover.apply(drag)

        if liquid.contains(mover):
            drag_coeff = -0.1
            drag = drag_coeff * liquid.density * mover.velocity * np.linalg.norm(mover.velocity)
            mover.apply(drag)

        mover.update(False)
        mover.draw(c)

    root.after(25, main)  # 40 fps


root = Tk()
root.title("Tkinter demo")
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#ffffff")
c.pack()
c.bind('<Motion>', mousemove)
c.bind('<Button-1>', mousedown)
c.bind('<ButtonRelease-1>', mouseup)
c.bind('<Button-2>', rmousedown)
c.bind('<ButtonRelease-3>', rmouseup)

liquid = Liquid()
movers = []
for i in range(10):
    movers.append(Mover())

main()
root.mainloop()
