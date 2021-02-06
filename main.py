import pygame

from constants import fps
from display import Display
from tetris import Tetris


def run():
    # Initialize the game engine
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Multris")

    game = Tetris()
    display = Display()

    # Loop until the user clicks the close button.
    pressing_down = False
    done = False
    counter = 0

    while not done:
        if game.figure is None:
            game.new_figure()

        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // game.level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_SPACE:
                    game.go_space()
                if event.key == pygame.K_ESCAPE:
                    game.__init__()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False

        display.display(game.score, game.state, game.figure, game.field)
        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    run()
