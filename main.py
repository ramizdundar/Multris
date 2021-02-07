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
    pressing_down = [False, False]
    done = False
    counter = 0

    while not done:
        counter += 1
        if counter > 100000:
            counter = 0

        for ix in range(2):
            if game.figures[ix] is None:
                game.new_figure(ix)
            if counter % (fps // game.level // 2) == 0 or pressing_down[ix]:
                if game.state == "start":
                    game.go_down(ix)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate(0)
                if event.key == pygame.K_DOWN:
                    pressing_down[0] = True
                if event.key == pygame.K_LEFT:
                    game.go_side(-1, 0)
                if event.key == pygame.K_RIGHT:
                    game.go_side(1, 0)
                if event.key == pygame.K_SPACE:
                    game.go_space(0)

                if event.key == pygame.K_w:
                    game.rotate(1)
                if event.key == pygame.K_s:
                    pressing_down[1] = True
                if event.key == pygame.K_a:
                    game.go_side(-1, 1)
                if event.key == pygame.K_d:
                    game.go_side(1, 1)
                if event.key == pygame.K_TAB:
                    game.go_space(1)

                if event.key == pygame.K_ESCAPE:
                    game.__init__()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down[0] = False
                if event.key == pygame.K_s:
                    pressing_down[1] = False

        display.display(game.score, game.state, game.figures, game.field)
        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    run()
