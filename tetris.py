from typing import List

from constants import tetris_x, tetris_y, tetris_zoom, tetris_level, tetris_height, tetris_width
from figure import Figure
from network import Network
from packet import Packet, PacketType


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
    network: Network

    def __init__(self, network):
        self.field = []
        self.score = 0
        self.state = "wait"
        self.remote_state = "wait"  # This state doesn't have to be accurate
        self.network = network
        self.network.connect_network_module_with_game_instance(self)

        for i in range(tetris_height):
            new_line = []
            for j in range(tetris_width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self, ix):
        self.figures[ix] = Figure(6 + 16 * ix, 0)
        self.figures[ix].color = ix + 1

    def intersects(self, ix):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figures[ix].image():
                    if i + self.figures[ix].y > self.height - 1 or \
                            j + self.figures[ix].x > self.width - 1 or \
                            j + self.figures[ix].x < 0 or \
                            self.field[i + self.figures[ix].y][j + self.figures[ix].x] > 0:
                        return True

        return False

    def intersects_with_other_figure(self, ix):
        other_figure = {}
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figures[1 - ix].image():
                    other_figure[str(i + self.figures[1 - ix].y) + "," + str(j + self.figures[1 - ix].x)] = 1

        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figures[ix].image():
                    if str(i + self.figures[ix].y) + "," + str(j + self.figures[ix].x) in other_figure:
                        return True

        return False

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
        while not (self.intersects(ix) or self.intersects_with_other_figure(ix)):
            self.figures[ix].y += 1
        if self.intersects(ix):
            self.figures[ix].y -= 1
            self.freeze(ix)
            self.send_remote(ix)
        else:
            self.figures[ix].y -= 1

    def go_down(self, ix):
        self.figures[ix].y += 1
        if self.intersects(ix):
            self.figures[ix].y -= 1
            self.freeze(ix)
        elif self.intersects_with_other_figure(ix):
            self.figures[ix].y -= 1
        self.send_remote(ix)

    def freeze(self, ix):
        self.send_freeze(ix)
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figures[ix].image():
                    self.field[i + self.figures[ix].y][j + self.figures[ix].x] = self.figures[ix].color
        self.break_lines()
        self.new_figure(ix)
        if self.intersects(ix):
            self.state = "gameover"
            self.send_state()

    def freeze_figure(self, figure):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in figure.image():
                    if self.field[i + figure.y][j + figure.x] > 0:
                        return
                    self.field[i + figure.y][j + figure.x] = figure.color
        self.break_lines()

    def go_side(self, dx, ix):
        old_x = self.figures[ix].x
        self.figures[ix].x += dx
        if self.intersects(ix) or self.intersects_with_other_figure(ix):
            self.figures[ix].x = old_x
        self.send_remote(ix)

    def rotate(self, ix):
        old_rotation = self.figures[ix].rotation
        self.figures[ix].rotate()
        if self.intersects(ix) or self.intersects_with_other_figure(ix):
            self.figures[ix].rotation = old_rotation
        self.send_remote(ix)

    def send_remote(self, ix):
        self.network.send_udp_packet(Packet(PacketType.FIGURE, self.figures[ix]), self.network.remote_address)

    def send_freeze(self, ix):
        packet = Packet(PacketType.FREEZE, self.figures[ix])
        self.network.send_udp_packet(packet, self.network.remote_address)
        self.network.send_udp_packet(packet, self.network.remote_address)
        self.network.send_udp_packet(packet, self.network.remote_address)

    def send_state(self):
        packet = Packet(PacketType.STATE, self.state)
        self.network.send_udp_packet(packet, self.network.remote_address)
        self.network.send_udp_packet(packet, self.network.remote_address)
        self.network.send_udp_packet(packet, self.network.remote_address)
