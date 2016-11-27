# coding=utf-8

from tkinter import *
import numpy as np
import random

WIDTH = 800
HEIGHT = 600
mousepos = np.array([WIDTH / 2, HEIGHT / 2])


class Mover:
    def __init__(self):
        self.position = np.array([WIDTH / 2.0, HEIGHT / 2.0])
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.BALL_RADIUS = 20
        self.mover = None

    def update(self, trail=False):
        self.acceleration = (mousepos - self.position) * 0.002

        print(self.acceleration)

        self.velocity += self.acceleration

        if trail:
            c.create_line(self.position[0], self.position[1],
                          self.position[0] + self.velocity[0],
                          self.position[1] + self.velocity[1],
                          width=self.BALL_RADIUS / 4, fill="red")

        self.position += self.velocity

        self.bounce()

    def draw(self, canvas):
        canvas.delete(self.mover)
        self.mover = canvas.create_oval(self.position[0] - self.BALL_RADIUS / 2,
                                        self.position[1] - self.BALL_RADIUS / 2,
                                        self.position[0] + self.BALL_RADIUS / 2,
                                        self.position[1] + self.BALL_RADIUS / 2,
                                        fill="Red")

    def bounce(self):
        if not (0 <= self.position[0] <= WIDTH):
            self.velocity[0] *= -1
        if not (0 <= self.position[1] <= HEIGHT):
            self.velocity[1] *= -1

    def toroid(self):
        self.position[0] = self.position[0] % WIDTH
        self.position[1] = self.position[1] % HEIGHT


def main():
    mover.update(True)
    mover.draw(c)
    root.after(25, main)  # 40 fps


def mousemove(event):
    global mousepos
    mousepos = np.array([event.x, event.y])


root = Tk()
root.title("Tkinter demo")
# область анимации
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#ffffff")
c.pack()
c.bind('<Motion>', mousemove)

mover = Mover()

main()
root.mainloop()
