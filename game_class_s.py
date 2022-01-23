"""
game class file for server
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
        # get settings when called by the server program
        self.screen = screen
        self.win_w = win_w
        self.win_h = win_h

        self.map_id = map_id
        self.current_level_no = level_id
        self.match_id = match_id

        # match score
        self.match_score = {"match_type": MATCH_TYPE_LST[self.match_id],
                            "round": 0, "shooter": 0, "chopper": 0,
                            "map": MAP_LST[self.map_id], "game_finished": False}

        """
        0   , 1        , 2         , 3   , 4     , 5             , 6
        quit, move_left, move_right, jump, attack, move_left_stop, move_right_stop
        """
        self.events_str_shooter = "0000000"
        self.events_str_chopper = "0000000"

        self.current_level = None

        self.bullets_l = []
        self.live_bullet_l = 0
        for i in range(TTL_BULLETS):
            bullet = Bullet(DEAD_BULLET_POS, 'l', SCREEN_WIDTH)
            self.bullets_l.append(bullet)

        self.bullets_r = []
        self.live_bullet_r = 0
        for i in range(TTL_BULLETS):
            bullet = Bullet(DEAD_BULLET_POS, 'r', SCREEN_WIDTH)
            self.bullets_r.append(bullet)

        # the "R" sign on the shooter's head to indicate it's the reloading time, so it can't shoot
        self.r_sign = DrawText(self.screen, 10, RED, 0, 0, "r_sign", "R", 0, 10)
        self.snd_yeet = False

        self.winner = None
        self.running = True
        self.playing = True

    def new(self):
        if self.match_score["game_finished"]:
            return
        else:
            self.match_score["round"] += 1

        self.restart()

    def restart(self):
        # match type
        match_type = self.match_score["match_type"]

        # start a new game


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

        self.active_sprite_grp = pg.sprite.Group()
        self.bullet_sprite_grp = pg.sprite.Group()

        self.player_shooter.level = self.current_level
        self.player_shooter.rect.x = 200
        self.player_shooter.rect.y = 0

        self.player_chopper.level = self.current_level
        self.player_chopper.rect.x = 600
        self.player_chopper.rect.y = 200

        self.live_bullet_l = 0
        self.live_bullet_r = 0
        for i in range(TTL_BULLETS):
            self.bullets_l[i].rect.x, self.bullets_l[i].rect.y = DEAD_BULLET_POS
            self.bullets_l[i].level = self.current_level
            self.bullets_r[i].rect.x, self.bullets_r[i].rect.y = DEAD_BULLET_POS
            self.bullets_r[i].level = self.current_level

        self.active_sprite_grp.add(self.player_shooter, self.player_chopper)
        self.bullet_sprite_grp.add(*self.bullets_r, *self.bullets_l)

        # self.run()
    #
    # def run(self):
    #     # Game Loop
    #     self.playing = True
    #     while self.playing:
    #         self.clock.tick(FPS)
    #         self.events()
    #         self.update()

    def events(self):
        # Game Loop - events
        lst_s = list(self.events_str_shooter)
        lst_c = list(self.events_str_chopper)

        events_lst_shooter = [int(item) for item in lst_s]
        events_lst_chopper = [int(item) for item in lst_c]

        if events_lst_shooter[0] or events_lst_chopper[0]:
            if self.playing:
                self.playing = False
            self.running = False
        if events_lst_shooter[1]:
            self.player_shooter.go_left()
        if events_lst_shooter[2]:
            self.player_shooter.go_right()
        if events_lst_shooter[3]:
            self.player_shooter.jump()
        if events_lst_shooter[4]:
            if self.player_shooter.loaded > 0:
                self.player_shooter.image_idx = 0
                self.player_shooter.loaded -= 1
                if self.player_shooter.direction == 'l':
                    self.bullets_l[self.live_bullet_l].rect.x = self.player_shooter.rect.x
                    self.bullets_l[self.live_bullet_l].rect.y = self.player_shooter.rect.y
                    self.bullets_l[self.live_bullet_l].live_flag = 1
                    self.player_shooter.attack_flg = 1
                    self.live_bullet_l += 1
                    # self.snd_yeet.play()
                else:
                    self.bullets_r[self.live_bullet_r].rect.x = self.player_shooter.rect.x
                    self.bullets_r[self.live_bullet_r].rect.y = self.player_shooter.rect.y
                    self.bullets_r[self.live_bullet_r].live_flag = 1
                    self.player_shooter.attack_flg = 1
                    self.live_bullet_r += 1
                    # self.snd_yeet.play()
                # self.bullets.append(bullet)
                # self.bullet_sprite_grp.add(bullet)

        if events_lst_chopper[1]:
            self.player_chopper.go_left()
        if events_lst_chopper[2]:
            self.player_chopper.go_right()
        if events_lst_chopper[3]:
            self.player_chopper.jump()
        if events_lst_chopper[4]:
            self.player_chopper.chop()
            self.player_chopper.image_idx = 0

        # player_shooter controls
        if events_lst_shooter[5] and self.player_shooter.change_x < 0:
            self.player_shooter.stop()
        if events_lst_shooter[6] and self.player_shooter.change_x > 0:
            self.player_shooter.stop()

        # player_chopper controls
        if events_lst_chopper[5] and self.player_chopper.change_x < 0:
            self.player_chopper.stop()
        if events_lst_chopper[6] and self.player_chopper.change_x > 0:
            self.player_chopper.stop()

    def update(self):
        # Game Loop - Update
        # Update the player.
        self.active_sprite_grp.update()
        self.bullet_sprite_grp.update()

        # Update the r_sign to follow the player_shooter
        if self.player_shooter.reload_timer > 0 and self.r_sign not in self.active_sprite_grp:
            self.r_sign.rect.midbottom = self.player_shooter.rect.midtop
            self.active_sprite_grp.add(self.r_sign)
        elif self.player_shooter.reload_timer == 0 and self.r_sign in self.active_sprite_grp:
            self.r_sign.rect.midbottom = DEAD_R_POS
            self.active_sprite_grp.remove(self.r_sign)

        if self.player_chopper in self.active_sprite_grp:
            bullet_hit_chopper = pg.sprite.spritecollideany(self.player_chopper, self.bullet_sprite_grp)
            if bullet_hit_chopper:
                bullet_hit_chopper.live_flag = 0
                self.player_chopper.hit_flag = 1
                self.player_chopper.hit_count += 1

                if self.player_chopper.hit_count == self.player_chopper.hit_limit:
                    # self.active_sprite_grp.remove(self.player_chopper)
                    self.match_score["shooter"] += 1
                    self.winner, self.playing = self.check_winner()
                    if self.winner is None:
                        self.restart()

            if pg.sprite.collide_rect(self.player_shooter, self.player_chopper):
                if self.player_shooter.hit_flag == 0 and self.player_chopper.chop_flag == 1:
                    self.player_shooter.hit_flag = 1
                    self.player_shooter.hit_count += 1
                    if self.player_shooter.hit_count >= self.player_shooter.hit_limit:
                        # self.active_sprite_grp.remove(self.player_shooter)
                        self.match_score["chopper"] += 1
                        self.winner, self.playing = self.check_winner()
                        if self.winner is None:
                            self.restart()

                elif self.player_shooter.hit_flag == 1 and self.player_chopper.chop_flag == 0:
                    self.player_shooter.hit_flag = 0

        for i in range(len(self.bullets_l)):
            if self.bullets_l[i].live_flag == 0:
                self.bullets_l[i].rect.x, self.bullets_l[i].rect.y = DEAD_BULLET_POS
            if self.bullets_r[i].live_flag == 0:
                self.bullets_r[i].rect.x, self.bullets_r[i].rect.y = DEAD_BULLET_POS

        # Update items in the level
        self.current_level.update()

    def check_winner(self):
        # return the winner role (if game over) or None, and a bool value for self.playing
        if self.match_score["match_type"] == MATCH_TYPE_LST[0]:
            # death match
            if self.match_score["shooter"] == 1:
                return "shooter", False
            elif self.match_score["chopper"] == 1:
                return "chopper", False
        elif self.match_score["match_type"] == MATCH_TYPE_LST[1]:
            # 1st23
            if self.match_score["shooter"] == 3:
                return "shooter", False
            elif self.match_score["chopper"] == 3:
                return "chopper", False
            else:
                return None, True
        elif self.match_score["match_type"] == MATCH_TYPE_LST[2]:
            # best of 3
            if self.match_score["shooter"] == 2 and self.match_score["chopper"] == 0:
                return "shooter", False
            elif self.match_score["chopper"] == 2 and self.match_score["shooter"] == 0:
                return "chopper", False
            elif self.match_score["shooter"] == 3:
                return "shooter", False
            elif self.match_score["chopper"] == 3:
                return "chopper", False
            else:
                return None, True