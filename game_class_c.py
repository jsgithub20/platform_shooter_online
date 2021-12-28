"""
game class file for client
"""

import pygame as pg
import pygame.freetype as ft
from sys import exit
from platform_shooter_settings import *
from platform_shooter_sprites import *
import sprite_player_correction
from role_def import *


class Game:
    def __init__(self, screen, win_w, win_h, map_id, level_id, match_id, role_id):
        pg.init()
        self.screen = screen
        self.win_w = win_w
        self.win_h = win_h

        self.map_id = map_id
        self.current_level_no = level_id
        self.match_id = match_id
        self.role_id = role_id

        self.events_str = "0000000"

        self.current_level = None

        self.bullets_l = []
        self.live_bullet_l = 0
        for i in range(TTL_BULLETS):
            bullet = Bullet(DEAD_BULLET_POS, 'l', SCREEN_WIDTH)
            bullet.level = self.current_level
            self.bullets_l.append(bullet)

        self.bullets_r = []
        self.live_bullet_r = 0
        for i in range(TTL_BULLETS):
            bullet = Bullet(DEAD_BULLET_POS, 'r', SCREEN_WIDTH)
            bullet.level = self.current_level
            self.bullets_r.append(bullet)

        # the "R" sign on the shooter's head to indicate it's the reloading time, so it can't shoot
        self.r_sign = DrawText(self.screen, 10, RED, 0, 0, "r_sign", "R", 0, 10)
        self.snd_yeet = False

        self.fps_txt = DrawText(self.screen, 5, LIGHT_GREEN, 5, 5, "fps_txt", "0")

        self.shooter_score = "0"
        self.chopper_score = "0"
        match_score = f"{self.shooter_score} - {MATCH_TYPE_LST(self.match_id)} - {self.chopper_score}"
        self.match_type_txt = DrawText(self.screen, 20, WHITE, 25, 720, "match_score", match_score, centered=True)
        self.snd_yeet = pg.mixer.Sound("resources/sound/yeet.ogg")
        self.snd_yeet.set_volume(0.2)

        self.winner = None
        self.running = True
        self.playing = True

    def new(self):
        pg.mixer.music.load("resources/sound/Resurrection of the Dagger.ogg")
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(loops=-1)

        self.restart()

    def restart(self):
        # start a new game
        self.live_bullet_l = 0
        self.live_bullet_r = 0
        for i in range(TTL_BULLETS):
            self.bullets_l[i].rect.x, self.bullets_l[i].rect.y = DEAD_BULLET_POS
            self.bullets_r[i].rect.x, self.bullets_r[i].rect.y = DEAD_BULLET_POS

        # Create the self.player
        self.player_shooter = Player()
        self.player_shooter.hit_limit = 3

        self.player_chopper = sprite_player_correction.Player()
        self.player_chopper.hit_limit = 3

        self.role_lst = [self.player_shooter, self.player_chopper]

        # Create all the levels
        self.level_list = []
        self.level01 = Level_01(self.player_shooter, self.player_chopper)
        self.level02 = Level_02(self.player_shooter, self.player_chopper)
        self.level_list.append(self.level01)
        self.level_list.append(self.level02)

        # Set the current level
        self.current_level = self.level_list[self.current_level_no]

        self.active_sprite_list = pg.sprite.Group()
        self.bullet_sprite_grp = pg.sprite.Group()

        self.player_shooter.level = self.current_level
        self.player_shooter.rect.x = 200
        self.player_shooter.rect.y = 0

        self.player_chopper.level = self.current_level
        self.player_chopper.rect.x = 600
        self.player_chopper.rect.y = 200

        self.active_sprite_list.add(self.player_shooter, self.player_chopper)
        self.bullet_sprite_grp.add(*self.bullets_r, *self.bullets_l)