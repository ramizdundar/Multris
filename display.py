import pygame

from constants import size, gray, colors, white, black
from tetris import Tetris


class Display:

    def __init__(self):
        self.game_score = 0
        self.game_state = ""
        self.game_figure = None
        self.game_field = []

        self.screen = pygame.display.set_mode(size)
        self.font = pygame.font.SysFont('arial', 25, False, False)
        self.big_font = pygame.font.SysFont('arial', 65, False, False)

    def display_reset(self):
        self.screen.fill(white)

    def display_field(self):
        for i in range(Tetris.height):
            for j in range(Tetris.width):
                pygame.draw.rect(self.screen, gray, [Tetris.x + Tetris.zoom * j,
                                                     Tetris.y + Tetris.zoom * i,
                                                     Tetris.zoom, Tetris.zoom], 1)
                if self.game_field[i][j] > 0:
                    pygame.draw.rect(self.screen, colors[self.game_field[i][j]], [Tetris.x + Tetris.zoom * j + 1,
                                                                                  Tetris.y + Tetris.zoom * i + 1,
                                                                                  Tetris.zoom - 2, Tetris.zoom - 1])

    def display_figure(self):
        if self.game_figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in self.game_figure.image():
                        pygame.draw.rect(self.screen, colors[self.game_figure.color],
                                         [Tetris.x + Tetris.zoom * (j + self.game_figure.x) + 1,
                                          Tetris.y + Tetris.zoom * (i + self.game_figure.y) + 1,
                                          Tetris.zoom - 2, Tetris.zoom - 2])

    def display_score(self):
        text = self.font.render("Score: " + str(self.game_score), True, black)
        self.screen.blit(text, [0, 0])

    def display_game_over_text(self):
        if self.game_state == "gameover":
            text_game_over = self.big_font.render("Game Over", True, (255, 125, 0))
            text_game_over1 = self.big_font.render("Press ESC", True, (255, 215, 0))
            self.screen.blit(text_game_over, [200, 200])
            self.screen.blit(text_game_over1, [25, 265])

    def update(self, game_score, game_state, game_figure, game_field):
        self.game_score = game_score
        self.game_state = game_state
        self.game_figure = game_figure
        self.game_field = game_field

    def display(self, game_score, game_state, game_figure, game_field):
        self.update(game_score, game_state, game_figure, game_field)
        self.display_reset()
        self.display_field()
        self.display_figure()
        self.display_score()
        self.display_game_over_text()
        pygame.display.flip()
