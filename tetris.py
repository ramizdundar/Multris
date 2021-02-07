from typing import List

from constants import tetris_x, tetris_y, tetris_zoom, tetris_level, tetris_height, tetris_width
from figure import Figure


class Tetris:
    # Static fields
    level = tetris_level
    x = tetris_x
    y = tetris_y
    zoom = tetris_zoom
    height = tetris_height
    width = tetris_width

    # Instance variables
    score: int
    state: str
    field: List[List[int]]
    figures: List[Figure] = [None, None]

    def __init__(self):
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(tetris_height):
            new_line = []
            for j in range(tetris_width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self, ix):
        self.figures[ix] = Figure(14, 0)
        self.figures[ix].color = ix + 1

    def intersects(self, ix):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figures[ix].image():
                    if i + self.figures[ix].y > self.height - 1 or \
                            j + self.figures[ix].x > self.width - 1 or \
                            j + self.figures[ix].x < 0 or \
                            self.field[i + self.figures[ix].y][j + self.figures[ix].x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self, ix):
        while not self.intersects(ix):
            self.figures[ix].y += 1
        self.figures[ix].y -= 1
        self.freeze(ix)

    def go_down(self, ix):
        self.figures[ix].y += 1
        if self.intersects(ix):
            self.figures[ix].y -= 1
            self.freeze(ix)

    def freeze(self, ix):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figures[ix].image():
                    self.field[i + self.figures[ix].y][j + self.figures[ix].x] = self.figures[ix].color
        self.break_lines()
        self.new_figure(ix)
        if self.intersects(ix):
            self.state = "gameover"

    def go_side(self, dx, ix):
        old_x = self.figures[ix].x
        self.figures[ix].x += dx
        if self.intersects(ix):
            self.figures[ix].x = old_x

    def rotate(self, ix):
        old_rotation = self.figures[ix].rotation
        self.figures[ix].rotate()
        if self.intersects(ix):
            self.figures[ix].rotation = old_rotation
