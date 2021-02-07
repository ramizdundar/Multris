import pygame

from constants import size, gray, colors, white, black
from figure import Figure
from tetris import Tetris


class Display:

    def __init__(self):
        self.game_score = 0
        self.game_state = ""
        self.game_figures = [Figure(0, 0), Figure(0, 0)]
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

    def display_figures(self):
        for ix in range(2):
            if self.game_figures[ix] is not None:
                for i in range(4):
                    for j in range(4):
                        p = i * 4 + j
                        if p in self.game_figures[ix].image():
                            pygame.draw.rect(self.screen, colors[self.game_figures[ix].color],
                                             [Tetris.x + Tetris.zoom * (j + self.game_figures[ix].x) + 1,
                                              Tetris.y + Tetris.zoom * (i + self.game_figures[ix].y) + 1,
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

    def update(self, game_score, game_state, game_figures, game_field):
        self.game_score = game_score
        self.game_state = game_state
        self.game_figures = game_figures
        self.game_field = game_field

    def display(self, game_score, game_state, game_figures, game_field):
        self.update(game_score, game_state, game_figures, game_field)
        self.display_reset()
        self.display_field()
        self.display_figures()
        self.display_score()
        self.display_game_over_text()
        pygame.display.flip()
