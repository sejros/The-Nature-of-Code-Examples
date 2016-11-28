# coding=utf-8

from math import sin, cos, pi, atan2, sqrt
from tkinter import *

import numpy as np

WIDTH = 800
HEIGHT = 600

mousepos = np.array([WIDTH / 2, HEIGHT / 2])
is_mouse_down = False
is_rmouse_down = False


class Pendulum:
    def __init__(self, anchor_x, anchor_y, lenght, radius):
        # self.position = np.array([WIDTH / 2.0, HEIGHT / 2.0])
        self.anchor = np.array([anchor_x, anchor_y])
        self.lenght = lenght
        self.raduis = radius

        self.angle = pi / 4
        self.ang_vel = 0.0
        self.ang_acc = 0.0

        self.bob = None
        self.arm = None

        self.mass = 1.0

        self.dragging = False

        self.bob_pos = self.anchor + np.array([self.lenght, 0])

    # def apply(self, force):
    #     self.acceleration += force / self.mass

    def run(self, canvas):
        self.update()

        if self.dragging:
            self.drag()

        self.draw(canvas)

    def update(self):
        self.ang_acc = - 0.5 * sin(self.angle) / self.lenght

        self.ang_vel += self.ang_acc
        self.ang_vel *= 0.999
        self.angle += self.ang_vel

        pos = np.array([sin(self.angle), cos(self.angle)])
        self.bob_pos = self.anchor + pos * self.lenght

    def draw(self, canvas):
        canvas.delete(self.arm)

        color = "grey"
        if self.dragging:
            color = "red"

        self.arm = canvas.create_line(self.bob_pos[0], self.bob_pos[1],
                                      self.anchor[0], self.anchor[1],
                                      width=self.raduis / 8, fill="grey")

        canvas.delete(self.bob)
        self.bob = canvas.create_oval(self.bob_pos[0] - self.raduis / 2,
                                      self.bob_pos[1] - self.raduis / 2,
                                      self.bob_pos[0] + self.raduis / 2,
                                      self.bob_pos[1] + self.raduis / 2,
                                      fill=color)

    def clicked(self, pos):
        dist = self.bob_pos - pos
        dist = sqrt(sum(dist * dist))
        print(dist)
        if dist <= self.raduis:
            self.dragging = True

    def stop_drag(self):
        self.ang_vel = 0.0
        self.dragging = False

    def drag(self):
        diff = mousepos - self.anchor
        self.angle = atan2(diff[0], diff[1])


def mousemove(event):
    global mousepos
    mousepos = np.array([event.x, event.y])


def mousedown(event):
    global is_mouse_down
    is_mouse_down = True
    pen.clicked(np.array([event.x, event.y]))


def mouseup(event):
    global is_mouse_down
    is_mouse_down = False
    pen.stop_drag()


def rmousedown(event):
    global is_rmouse_down
    is_rmouse_down = True


def rmouseup(event):
    global is_rmouse_down
    is_rmouse_down = False


def main():
    pen.run(c)

    gravity = np.array([0, 0.2]) * pen.mass
    # pen.apply(gravity)

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

pen = Pendulum(WIDTH / 2, 100, 300, 40)

main()
root.mainloop()
