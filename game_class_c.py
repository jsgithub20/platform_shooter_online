"""
game class file for client
"""

import pygame as pg
from sys import exit
from platform_shooter_settings import *
from platform_shooter_sprites import *
import sprite_player_correction
from role_def import *


class Game:
    def __init__(self, screen, win_w, win_h, map_id, level_id, match_id):
        pg.init()
        self.screen = screen
        self.win_w = win_w
        self.win_h = win_h

        self.map_id = map_id
        self.current_level_no = level_id
        self.match_id = match_id

