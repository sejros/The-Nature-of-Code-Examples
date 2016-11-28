# coding=utf-8

from math import sqrt
from tkinter import *

import numpy as np

WIDTH = 800
HEIGHT = 600

mousepos = np.array([WIDTH / 2, HEIGHT / 2])
is_mouse_down = False
is_rmouse_down = False


def mousemove(event):
    global mousepos
    mousepos = np.array([event.x, event.y])


def mousedown(event):
    global is_mouse_down
    is_mouse_down = True
    bob.clicked(np.array([event.x, event.y]))


def mouseup(event):
    global is_mouse_down
    is_mouse_down = False
    bob.stop_drag()


def rmousedown(event):
    global is_rmouse_down
    is_rmouse_down = True


def rmouseup(event):
    global is_rmouse_down
    is_rmouse_down = False


root = Tk()
root.title("Tkinter demo")
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#ffffff")
c.pack()
c.bind('<Motion>', mousemove)
c.bind('<Button-1>', mousedown)
c.bind('<ButtonRelease-1>', mouseup)
c.bind('<Button-2>', rmousedown)
c.bind('<ButtonRelease-3>', rmouseup)


class Draggable:
    dragging = False
    radius = 0
    position = None
    velocity = None

    def drag(self, mousepos):
        diff = (mousepos - self.position) * 0.5
        # print(diff)
        # self.angle = atan2(diff[0], diff[1])
        self.apply(diff)

    def clicked(self, pos):
        dist = self.position - pos
        dist = sqrt(sum(dist * dist))
        # print(dist)
        if dist <= self.radius:
            self.dragging = True

    def stop_drag(self):
        self.dragging = False

    def run(self):
        if self.dragging:
            self.drag(mousepos)


class Mover(Draggable):
    def __init__(self, pos):
        self.position = pos
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.mover = None
        self.mass = 1.0
        # self.mass = random.uniform(0.5, 2.0)
        self.radius = 20 * self.mass

    def apply(self, force):
        self.acceleration += force / self.mass

    def update(self, trail=False):

        self.velocity += self.acceleration

        if trail:
            c.create_line(self.position[0], self.position[1],
                          self.position[0] + self.velocity[0],
                          self.position[1] + self.velocity[1],
                          width=self.radius / 4, fill="red")

        self.position += self.velocity

        self.acceleration = np.array([0.0, 0.0])

    def draw(self, canvas):
        canvas.delete(self.mover)
        self.mover = canvas.create_oval(self.position[0] - self.radius / 2,
                                        self.position[1] - self.radius / 2,
                                        self.position[0] + self.radius / 2,
                                        self.position[1] + self.radius / 2,
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


class Spring:
    def __init__(self, origin, rest, k=0.1):
        self.origin = origin
        self.rest_length = rest
        self.k = k

        self.bob = None
        self.arm = None

    def attach(self, bob):
        self.bob = bob

    def update(self):
        dir = bob.position - self.origin
        current_length = sqrt(sum(dir * dir))
        dir /= current_length
        stretch = current_length - self.rest_length

        spring_force = -self.k * stretch * dir
        self.bob.apply(spring_force)

    def draw(self, c):
        c.delete(self.arm)
        self.arm = c.create_line(self.origin[0], self.origin[1],
                                 self.bob.position[0], self.bob.position[1])


def main():
    bob.run()
    spring.draw(c)
    spring.update()

    # wind = np.array([0.1, 0])
    # if is_mouse_down:
    #     bob.apply(wind)
    #
    gravity = np.array([0, 0.2]) * bob.mass
    bob.apply(gravity)

    drag_coeff = -0.005
    drag = drag_coeff * bob.velocity * np.linalg.norm(bob.velocity)
    bob.apply(drag)

    bob.update()
    bob.draw(c)

    root.after(25, main)  # 40 fps


bob = Mover(np.array([WIDTH / 2, 300]))
spring = Spring(origin=np.array([WIDTH / 2, 0]), rest=200)
spring.attach(bob)

main()
root.mainloop()
