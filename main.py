import os

import pygame

import player
from constants import fps, local_port
from display import Display
from network import Network
from packet import Packet, PacketType
from tetris import Tetris


def run():
    # Initialize the game engine
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Multris")

    network = Network(1 - player.player, "Ramiz")  # Other player is 1 - player
    network.run()
    network.discover()
    game = Tetris(network)
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
            if (counter % (fps // game.level // 2) == 0 and ix == player.player) or pressing_down[ix]:
                if game.state == "start":
                    game.go_down(ix)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if game.state == "start":
                        game.rotate(player.player)
                if event.key == pygame.K_DOWN:
                    pressing_down[player.player] = True
                if event.key == pygame.K_LEFT:
                    if game.state == "start":
                        game.go_side(-1, player.player)
                if event.key == pygame.K_RIGHT:
                    if game.state == "start":
                        game.go_side(1, player.player)
                if event.key == pygame.K_SPACE:
                    if game.state == "start":
                        game.go_space(player.player)

                if event.key == pygame.K_ESCAPE:
                    game.__init__(network)

                if event.key == pygame.K_r:
                    game.state = "ready"
                    if game.remote_state == "ready":
                        game.state = "start"
                    game.send_state()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down[player.player] = False

        display.display(game.score, game.state, game.figures, game.field)
        clock.tick(fps)

    for i in range(os.cpu_count() + 4):
        network.send_udp_packet(Packet(PacketType.QUIT), (network.local_ip, local_port))
    pygame.quit()


if __name__ == '__main__':
    run()
