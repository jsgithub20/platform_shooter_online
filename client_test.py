import pygame
import json
from network1 import Network

pygame.init()
width = 500
height = 500
win = pygame.display.set_mode((width, height))


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3


def main():
    n = Network("192.168.3.10", 5050)
    player_id = n.game_state.current_player
    game_id = n.game_state.game_id
    pygame.display.set_caption(f"Game: {str(game_id)}, Player: {str(player_id)}")
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        # try:
        #     game = n.send("get")
        # except:
        #     run = False
        #     print("Couldn't get game")
        #     break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()

main()