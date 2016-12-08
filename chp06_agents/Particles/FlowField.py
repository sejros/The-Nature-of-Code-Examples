from math import pi, sin, cos

import pygame
from noise import pnoise2, pnoise3
from numpy import array as vector
from math import ceil, floor

from Globals import WIDTH, HEIGHT


class FlowField:
    def __init__(self, resolution=50):
        self.field = []
        self.resolution = resolution
        self.cols = int(WIDTH / self.resolution)
        self.rows = int(HEIGHT / self.resolution)
        for i in range(self.cols):
            row = []
            for j in range(self.rows):
                row.append(vector((10, 0)))
            self.field.append(row)

    def lookup(self, location):
        col = int(location[0] / self.resolution) % self.cols - 1
        row = int(location[1] / self.resolution) % self.rows - 1
        return self.field[col][row]

    def draw(self, scr):
        for i in range(self.cols):
            for j in range(self.rows):
                center = vector((int((i + 0.5) * self.resolution),
                                 int((j + 0.5) * self.resolution)))
                pygame.draw.circle(scr, (255, 255, 0), center,
                                   ceil(self.resolution / 8), 1)
                pygame.draw.line(scr, (255, 255, 0),
                                 center, center + self.field[i][j], 1)


class PerlinField(FlowField):
    def __init__(self):
        super().__init__()
        self.toff = 0
        self.generate()

    def update(self):
        self.toff += 0.01
        self.generate()

    def generate(self):
        delta = 0.05
        xoff, yoff = 0, 0
        for i in range(self.cols):
            yoff = 0
            for j in range(self.rows):
                angle = pnoise3(xoff, yoff, self.toff) * 2 * pi
                self.field[i][j] = vector((sin(angle), cos(angle))) * 20
                yoff += delta
            xoff += delta


class PathField(FlowField):
    def __init__(self, path):
        super().__init__(path.raduis)
        for i in range(self.cols):
            for j in range(self.rows):
                center = vector((int((i + 1.5) * self.resolution),
                                 int((j + 1.5) * self.resolution)))
                self.field[i][j] = (path.get_normal(center) - center) * 0.2


class Grid:
    def __init__(self, resolution=40):
        self.resolution = resolution
        self.cols = int(WIDTH / self.resolution)
        self.rows = int(HEIGHT / self.resolution)
        self.objects = []
        self._init()

    def __iter__(self):
        return iter(self.objects)

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, index):
        return self.objects[index]

    def _init(self):
        self.grid = []
        for i in range(self.cols):
            row = []
            for j in range(self.rows):
                row.append([])
            self.grid.append(row)

    def append(self, obj):
        self.objects.append(obj)
        self._add_object(obj)

    def _add_object(self, obj):
        col = floor(obj.position[0] / self.resolution)
        row = floor(obj.position[1] / self.resolution)
        if 0 <= col < self.cols and 0 <= row < self.rows:
            (self.grid[col][row]).append(obj)

    def update(self):
        self._init()
        for obj in self.objects:
            self._add_object(obj)

    def nearest(self, pos, radius=40):
        col = floor(pos[0] / self.resolution)
        row = floor(pos[1] / self.resolution)

        n = ceil(radius / self.resolution)
        arr = vector(range(2 * n + 1)) - n

        res = []
        for i in arr:
            for j in arr:
                app = []
                try:
                    app = self.grid[col + i][row + j]
                    res.extend(self.grid[col + i][row + j])
                except IndexError:
                    pass

        return res

    def draw_cell(self, col, row, screen):
        x = (col) * self.resolution
        y = (row) * self.resolution
        w = self.resolution
        pygame.draw.rect(screen, (255, 0, 0), [x, y, w, w], 1)

    def draw(self, scr):
        pos = 0
        for i in range(self.cols):
            pos += self.resolution
            pygame.draw.line(scr, (255, 255, 0), (pos, 0), (pos, HEIGHT), 1)
        pos = 0
        for i in range(self.rows):
            pos += self.resolution
            pygame.draw.line(scr, (255, 255, 0), (0, pos), (WIDTH, pos), 1)
