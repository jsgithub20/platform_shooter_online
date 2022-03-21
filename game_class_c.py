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
    def __init__(self, screen, win_w, win_h, map_id, match_id, role_id, my_name, your_name):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = screen
        self.win_w = win_w
        self.win_h = win_h

        self.map_id = map_id
        self.current_level_no = 0
        self.match_id = match_id
        self.role_id = role_id
        self.my_name = my_name
        self.your_name = your_name

        """
        0   , 1        , 2         , 3   , 4     , 5             , 6
        quit, move_left, move_right, jump, attack, move_left_stop, move_right_stop
        """

        self.events_str = "0000000"
        self.events_lst = ["0", "0", "0", "0", "0", "0", "0"]

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
        self.r_sign = DrawText(self.screen, 30, RED, 0, 0, "r_sign", "R", 0, 10)
        self.snd_yeet = False

        self.fps_txt = DrawText(self.screen, 20, LIGHT_GREEN, 5, 5, "fps_txt", "0")

        self.shooter_score = "0"
        self.chopper_score = "0"
        match_score = f"{self.shooter_score} - {MATCH_TYPE_LST[int(self.match_id)]} - {self.chopper_score}"
        self.level_txt = DrawText(self.screen, 30, WHITE, 20, 10, "level", f"Level {self.current_level_no}", alignment="center")
        self.match_type_txt = DrawText(self.screen, 30, WHITE, 25, 720, "match_score", match_score, alignment="center")

        if self.role_id == "0":
            self.my_name_txt = DrawText(self.screen, 30, WHITE, 25, 720, "my_name", self.my_name, alignment="left")
            self.your_name_txt = DrawText(self.screen, 30, WHITE, 25, 720, "your_name", self.your_name, alignment="right")
        elif self.role_id == "1":
            self.my_name_txt = DrawText(self.screen, 30, WHITE, 25, 720, "my_name", self.my_name, alignment="right")
            self.your_name_txt = DrawText(self.screen, 30, WHITE, 25, 720, "your_name", self.your_name, alignment="left")

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
        self.level_txt.text = f"Level {self.current_level_no}"

        self.active_sprite_grp = pg.sprite.Group()
        self.bullet_sprite_grp = pg.sprite.Group()
        self.upd_text_sprite_grp = pg.sprite.Group()
        self.idle_text_sprite_grp = pg.sprite.Group()

        self.player_shooter.level = self.current_level
        self.player_shooter.rect.x = 200
        self.player_shooter.rect.y = 0

        self.player_chopper.level = self.current_level
        self.player_chopper.rect.x = 600
        self.player_chopper.rect.y = 200

        self.active_sprite_grp.add(self.player_shooter, self.player_chopper, self.r_sign)
        self.upd_text_sprite_grp.add(self.fps_txt, self.match_type_txt)  # only text sprites that need to be updated
        self.idle_text_sprite_grp.add(self.my_name_txt, self.your_name_txt, self.level_txt)
        self.bullet_sprite_grp.add(*self.bullets_r, *self.bullets_l)

    def events(self):
        # Game Loop - events
        for i in range(len(self.events_lst)):
            self.events_lst[i] = "0"
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.events_lst[0] = "1"
                self.playing = False

            if event.type == pg.KEYDOWN:
                # player_shooter controls
                if event.key == pg.K_LEFT:
                    self.events_lst[1] = "1"
                if event.key == pg.K_RIGHT:
                    self.events_lst[2] = "1"
                if event.key == pg.K_UP:
                    self.events_lst[3] = "1"
                if event.key == pg.K_SPACE:
                    self.events_lst[4] = "1"
                    # self.snd_yeet.play()

                # player_chopper controls
                if event.key == pg.K_a:
                    self.events_lst[1] = "1"
                elif event.key == pg.K_d:
                    self.events_lst[2] = "1"
                if event.key == pg.K_w:
                    self.events_lst[3] = "1"
                if event.key == pg.K_c:
                    self.events_lst[4] = "1"

            if event.type == pg.KEYUP:
                # player_shooter controls
                if event.key == pg.K_LEFT:
                    self.events_lst[5] = "1"
                if event.key == pg.K_RIGHT:
                    self.events_lst[6] = "1"

                # player_chopper controls
                if event.key == pg.K_a:
                    self.events_lst[5] = "1"
                if event.key == pg.K_d:
                    self.events_lst[6] = "1"

        self.events_str = "".join(self.events_lst)

    def update_game_state(self, gs_lst):
        self.clock.tick()
        if gs_lst[24] != "nobody":
            self.playing = False
        self.player_shooter.update_img(gs_lst[0], gs_lst[1])
        self.player_shooter.rect.x, self.player_shooter.rect.y = gs_lst[2]
        self.player_chopper.update_img(gs_lst[3], gs_lst[4])
        self.player_chopper.rect.x, self.player_chopper.rect.y = gs_lst[5]
        for i in range(TTL_BULLETS):
            self.bullets_l[i].rect.x, self.bullets_l[i].rect.y = gs_lst[i+6]
            self.bullets_r[i].rect.x, self.bullets_r[i].rect.y = gs_lst[i+11]
        if self.current_level_no == 1:
            self.current_level.moving_block.rect.x, self.current_level.moving_block.rect.y = gs_lst[16]
        if gs_lst[17]:  # r_sign_flg = 1
            self.r_sign.rect.midbottom = self.player_shooter.rect.midtop
        else:  # r_sign_flg = 0
            self.r_sign.rect.midbottom = (-99, -99)

        # {self.shooter_score} - {MATCH_TYPE_LST[int(self.match_id)]} - {self.chopper_score}
        self.match_type_txt.text = f"{gs_lst[22]} - {MATCH_TYPE_LST[int(gs_lst[19])]} - {gs_lst[23]}"
        self.fps_txt.text = str(int(self.clock.get_fps()))
        self.upd_text_sprite_grp.update()

    def draw(self):
        self.current_level.draw(self.screen)
        self.active_sprite_grp.draw(self.screen)
        self.bullet_sprite_grp.draw(self.screen)
        self.upd_text_sprite_grp.draw(self.screen)
        self.idle_text_sprite_grp.draw(self.screen)

        pg.display.update()