# coding=utf-8

from tkinter import *

import numpy as np

WIDTH = 800
HEIGHT = 600

mousepos = np.array([WIDTH / 2, HEIGHT / 2])
is_mouse_down = False
is_rmouse_down = False


def mousemove(event):
    global mousepos
    mousepos = np.array([float(event.x), float(event.y)])


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


root = Tk()
root.title("Tkinter demo")
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#ffffff")
c.pack()
c.bind('<Motion>', mousemove)
c.bind('<Button-1>', mousedown)
c.bind('<ButtonRelease-1>', mouseup)
c.bind('<Button-2>', rmousedown)
c.bind('<ButtonRelease-3>', rmouseup)


def main():
    root.after(25, main)  # 40 fps


# bob = Mover(np.array([WIDTH/2, 300]))
# spring = Spring(origin=np.array([WIDTH/2, 0]), rest=200)
# spring.attach(bob)

main()
root.mainloop()
