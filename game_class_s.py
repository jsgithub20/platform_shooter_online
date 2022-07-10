"""
game class file for server
"""

import pygame as pg
from sys import exit
from platform_shooter_settings import *
from platform_shooter_sprites import *
import sprite_player_correction
from role_def import *



class GameSC:  # shooter vs chopper
    def __init__(self, screen, win_w, win_h, map_id, level_id, match_id):
        pg.init()
        # get settings when called by the server program
        self.screen = screen
        self.win_w = win_w
        self.win_h = win_h

        self.map_id = map_id
        # self.current_level_no = level_id
        self.current_level_no = map_id
        self.match_id = match_id
        self.new_round = False

        # match score
        self.match_score = {"match_type": MATCH_TYPE_LST[self.match_id],
                            "round": 1, "shooter": 0, "chopper": 0,
                            "map": MAP_LST[self.map_id], "game_finished": False}

        """
        0   , 1        , 2         , 3   , 4     , 5             , 6
        quit, move_left, move_right, jump, attack, move_left_stop, move_right_stop
        """
        self.events_str0 = "0000000"
        self.events_str1 = "0000000"
        self.events_lst0 = list(self.events_str0)
        self.events_lst1 = list(self.events_str1)
        # self.game_state = []

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
        # self.r_sign = DrawText(self.screen, 10, RED, 0, 0, "r_sign", "R", 0, 10)
        self.r_sign_flg = 0
        self.snd_yeet = False

        self.running = True

    def new(self):
        self.winner = "nobody"
        self.playing = True
        self.match_score = {"match_type": MATCH_TYPE_LST[self.match_id],
                            "round": 0, "shooter": 0, "chopper": 0,
                            "map": MAP_LST[self.map_id], "game_finished": False}

        # if self.match_score["game_finished"]:
        #     return
        # else:
        #     self.match_score["round"] += 1

        self.restart()

    def restart(self):
        # match type
        match_type = self.match_score["match_type"]

        # initialize variables
        self.match_score["round"] += 1

        # Create the self.player
        self.player_shooter = Player()
        self.player_shooter.hit_limit = SHOOTER_SCORE_HIT

        self.player_chopper = sprite_player_correction.Player()
        self.player_chopper.hit_limit = CHOPPER_SCORE_HIT

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
        self.player_shooter.rect.y = -50

        self.player_chopper.level = self.current_level
        self.player_chopper.rect.x = 700
        self.player_chopper.rect.y = -50

        self.live_bullet_l = 0
        self.live_bullet_r = 0
        for i in range(TTL_BULLETS):
            self.bullets_l[i].rect.x, self.bullets_l[i].rect.y = DEAD_BULLET_POS
            self.bullets_l[i].level = self.current_level
            self.bullets_r[i].rect.x, self.bullets_r[i].rect.y = DEAD_BULLET_POS
            self.bullets_r[i].level = self.current_level

        self.r_sign_flg = 0

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
        # lst_s = list(self.events_str_shooter)
        # lst_c = list(self.events_str_chopper)

        events_lst_shooter = [int(item) for item in self.events_lst0]
        events_lst_chopper = [int(item) for item in self.events_lst1]

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
                    for bullet in iter(self.bullets_l):
                        if not bullet.live_flag:
                            bullet.rect.x = self.player_shooter.rect.x
                            bullet.rect.y = self.player_shooter.rect.y
                            bullet.live_flag = 1
                            break
                    self.player_shooter.attack_flg = 1
                    # self.snd_yeet.play()
                else:
                    for bullet in iter(self.bullets_r):
                        if not bullet.live_flag:
                            bullet.rect.x = self.player_shooter.rect.x
                            bullet.rect.y = self.player_shooter.rect.y
                            bullet.live_flag = 1
                            break
                    self.player_shooter.attack_flg = 1
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

        if self.player_shooter.reload_timer > 0 and not self.r_sign_flg:
            self.r_sign_flg = 1
        elif self.player_shooter.reload_timer == 0 and self.r_sign_flg:
            self.r_sign_flg = 0

        if self.player_chopper in self.active_sprite_grp:
            bullet_hit_chopper = pg.sprite.spritecollideany(self.player_chopper, self.bullet_sprite_grp)
            if bullet_hit_chopper:
                bullet_hit_chopper.live_flag = 0
                # self.player_chopper.hit_flag = 1
                self.player_chopper.hit_count += 1

                if self.player_chopper.hit_count == self.player_chopper.hit_limit:
                    # self.active_sprite_grp.remove(self.player_chopper)
                    self.match_score["shooter"] += 1
                    # self.player_chopper.hit_count = 0
                    self.winner, self.playing = self.check_winner()
                    if self.winner == "nobody":
                        # self.match_score["round"] += 1
                        self.new_round = True

            if pg.sprite.collide_rect(self.player_shooter, self.player_chopper):
                if self.player_shooter.hit_flag == 0 and self.player_chopper.chop_flag == 1:
                    self.player_shooter.hit_flag = 1
                    self.player_shooter.hit_count += 1
                    if self.player_shooter.hit_count == self.player_shooter.hit_limit:
                        # self.active_sprite_grp.remove(self.player_shooter)
                        self.match_score["chopper"] += 1
                        # self.player_shooter.hit_count = 0
                        self.winner, self.playing = self.check_winner()
                        if self.winner == "nobody":
                            # self.match_score["round"] += 1
                            self.new_round = True

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
        # return the winner role (if game over) or "nobody", and a bool value for self.playing
        self.match_score["match_type"] = MATCH_TYPE_LST[self.match_id]
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
                return "nobody", True
        elif self.match_score["match_type"] == MATCH_TYPE_LST[2]:
            # best of 3
            if self.match_score["shooter"] == 2:
                return "shooter", False
            elif self.match_score["chopper"] == 2:
                return "chopper", False
            # elif self.match_score["shooter"] == 3:
            #     return "shooter", False
            # elif self.match_score["chopper"] == 3:
            #     return "chopper", False
            else:
                return "nobody", True

    def gs_conversion(self):
        game_state = []
        game_state.append(self.player_shooter.img_dict_key)
        game_state.append(self.player_shooter.image_idx)
        game_state.append((self.player_shooter.rect.x, self.player_shooter.rect.y))
        game_state.append(self.player_chopper.img_dict_key)
        game_state.append(self.player_chopper.image_idx)
        game_state.append((self.player_chopper.rect.x, self.player_chopper.rect.y))
        game_state.append((self.bullets_l[0].rect.x, self.bullets_l[0].rect.y))
        game_state.append((self.bullets_l[1].rect.x, self.bullets_l[1].rect.y))
        game_state.append((self.bullets_l[2].rect.x, self.bullets_l[2].rect.y))
        game_state.append((self.bullets_l[3].rect.x, self.bullets_l[3].rect.y))
        game_state.append((self.bullets_l[4].rect.x, self.bullets_l[4].rect.y))
        game_state.append((self.bullets_r[0].rect.x, self.bullets_r[0].rect.y))
        game_state.append((self.bullets_r[1].rect.x, self.bullets_r[1].rect.y))
        game_state.append((self.bullets_r[2].rect.x, self.bullets_r[2].rect.y))
        game_state.append((self.bullets_r[3].rect.x, self.bullets_r[3].rect.y))
        game_state.append((self.bullets_r[4].rect.x, self.bullets_r[4].rect.y))
        if self.current_level_no == 0:
            game_state.append(DEAD_CRATER_POS)
        else:
            game_state.append((self.level02.moving_block.rect.x, self.level02.moving_block.rect.y))
        game_state.append(self.r_sign_flg)
        game_state.append(self.map_id)
        game_state.append(self.match_id)
        game_state.append(self.current_level_no)
        game_state.append(self.match_score["round"])
        game_state.append(self.match_score["shooter"])
        game_state.append(self.match_score["chopper"])
        game_state.append(self.winner)
        game_state.append(self.player_shooter.hit_count)
        game_state.append(self.player_chopper.hit_count)

        return game_state


class GameSS:  # shooter vs shooter
    def __init__(self, screen, win_w, win_h, map_id, level_id, match_id):
        pg.init()
        # get settings when called by the server program
        self.screen = screen
        self.win_w = win_w
        self.win_h = win_h

        self.map_id = map_id
        # self.current_level_no = level_id
        self.current_level_no = map_id
        self.match_id = match_id
        self.new_round = False

        # match score
        self.match_score = {"match_type": MATCH_TYPE_LST[self.match_id],
                            "round": 1, "shooter0": 0, "shooter1": 0,
                            "map": MAP_LST[self.map_id], "game_finished": False}

        """
        0   , 1        , 2         , 3   , 4     , 5             , 6
        quit, move_left, move_right, jump, attack, move_left_stop, move_right_stop
        """
        self.events_str0 = "0000000"
        self.events_str1 = "0000000"
        self.events_lst0 = list(self.events_str0)
        self.events_lst1 = list(self.events_str1)

        self.current_level = None

        self.bullets_l0 = []
        self.live_bullet_l0 = 0
        self.bullets_l1 = []
        self.live_bullet_l1 = 0
        for i in range(TTL_BULLETS):
            bullet0 = Bullet(DEAD_BULLET_POS, 'l', SCREEN_WIDTH)
            self.bullets_l0.append(bullet0)
            bullet1 = Bullet(DEAD_BULLET_POS, 'l', SCREEN_WIDTH)
            self.bullets_l1.append(bullet1)

        self.bullets_r0 = []
        self.live_bullet_r0 = 0
        self.bullets_r1 = []
        self.live_bullet_r1 = 0
        for i in range(TTL_BULLETS):
            bullet0 = Bullet(DEAD_BULLET_POS, 'r', SCREEN_WIDTH)
            self.bullets_r0.append(bullet0)
            bullet1 = Bullet(DEAD_BULLET_POS, 'r', SCREEN_WIDTH)
            self.bullets_r1.append(bullet1)

        # the "R" sign on the shooter's head to indicate it's the reloading time, so it can't shoot
        # self.r_sign = DrawText(self.screen, 10, RED, 0, 0, "r_sign", "R", 0, 10)
        self.r_sign_flg0 = 0
        self.r_sign_flg1 = 0
        self.snd_yeet = False

        self.running = True

    def new(self):
        self.winner = "nobody"
        self.playing = True
        self.match_score = {"match_type": MATCH_TYPE_LST[self.match_id],
                            "round": 0, "shooter0": 0, "shooter1": 0,
                            "map": MAP_LST[self.map_id], "game_finished": False}

        # if self.match_score["game_finished"]:
        #     return
        # else:
        #     self.match_score["round"] += 1

        self.restart()

    def restart(self):
        # match type
        match_type = self.match_score["match_type"]

        # initialize variables
        self.match_score["round"] += 1

        # Create the self.player
        self.player_shooter0 = Player()
        self.player_shooter0.hit_limit = SS_SHOOTER_SCORE_HIT

        self.player_shooter1 = Player()
        self.player_shooter1.hit_limit = SS_SHOOTER_SCORE_HIT

        self.role_lst = [self.player_shooter0, self.player_shooter1]

        # Create all the levels
        self.level_list = []
        self.level01 = Level_01(self.player_shooter0, self.player_shooter1)
        self.level02 = Level_02(self.player_shooter0, self.player_shooter1)
        self.level_list.append(self.level01)
        self.level_list.append(self.level02)

        # Set the current level
        self.current_level = self.level_list[self.current_level_no]

        self.active_sprite_grp = pg.sprite.Group()
        self.bullet_sprite_grp0 = pg.sprite.Group()
        self.bullet_sprite_grp1 = pg.sprite.Group()

        self.player_shooter0.level = self.current_level
        self.player_shooter0.rect.x = 200
        self.player_shooter0.rect.y = -50

        self.player_shooter1.level = self.current_level
        self.player_shooter1.rect.x = 700
        self.player_shooter1.rect.y = -50

        self.live_bullet_l0 = 0
        self.live_bullet_r0 = 0
        self.live_bullet_l1 = 0
        self.live_bullet_r1 = 0
        for i in range(TTL_BULLETS):
            self.bullets_l0[i].rect.x, self.bullets_l0[i].rect.y = DEAD_BULLET_POS
            self.bullets_l0[i].level = self.current_level
            self.bullets_r0[i].rect.x, self.bullets_r0[i].rect.y = DEAD_BULLET_POS
            self.bullets_r0[i].level = self.current_level

            self.bullets_l1[i].rect.x, self.bullets_l1[i].rect.y = DEAD_BULLET_POS
            self.bullets_l1[i].level = self.current_level
            self.bullets_r1[i].rect.x, self.bullets_r1[i].rect.y = DEAD_BULLET_POS
            self.bullets_r1[i].level = self.current_level

        self.r_sign_flg0 = 0
        self.r_sign_flg1 = 0

        self.active_sprite_grp.add(self.player_shooter0, self.player_shooter1)
        self.bullet_sprite_grp0.add(*self.bullets_r0, *self.bullets_l0)
        self.bullet_sprite_grp1.add(*self.bullets_r1, *self.bullets_l1)

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
        # lst_s = list(self.events_str_shooter0)
        # lst_c = list(self.events_str_shooter1)

        events_lst_shooter0 = [int(item) for item in self.events_lst0]
        events_lst_shooter1 = [int(item) for item in self.events_lst1]

        if events_lst_shooter0[0] or events_lst_shooter1[0]:
            if self.playing:
                self.playing = False
            self.running = False
        if events_lst_shooter0[1]:
            self.player_shooter0.go_left()
        if events_lst_shooter0[2]:
            self.player_shooter0.go_right()
        if events_lst_shooter0[3]:
            self.player_shooter0.jump()
        if events_lst_shooter0[4]:
            if self.player_shooter0.loaded > 0:
                self.player_shooter0.image_idx = 0
                self.player_shooter0.loaded -= 1
                if self.player_shooter0.direction == 'l':
                    for bullet in iter(self.bullets_l0):
                        if not bullet.live_flag:
                            bullet.rect.x = self.player_shooter0.rect.x
                            bullet.rect.y = self.player_shooter0.rect.y
                            bullet.live_flag = 1
                            break
                    self.player_shooter0.attack_flg = 1
                    # self.snd_yeet.play()
                else:
                    for bullet in iter(self.bullets_r0):
                        if not bullet.live_flag:
                            bullet.rect.x = self.player_shooter0.rect.x
                            bullet.rect.y = self.player_shooter0.rect.y
                            bullet.live_flag = 1
                            break
                    self.player_shooter0.attack_flg = 1
                    # self.snd_yeet.play()

        if events_lst_shooter1[1]:
            self.player_shooter1.go_left()
        if events_lst_shooter1[2]:
            self.player_shooter1.go_right()
        if events_lst_shooter1[3]:
            self.player_shooter1.jump()
        if events_lst_shooter1[4]:
            if self.player_shooter1.loaded > 0:
                self.player_shooter1.image_idx = 0
                self.player_shooter1.loaded -= 1
                if self.player_shooter1.direction == 'l':
                    for bullet in iter(self.bullets_l1):
                        if not bullet.live_flag:
                            bullet.rect.x = self.player_shooter1.rect.x
                            bullet.rect.y = self.player_shooter1.rect.y
                            bullet.live_flag = 1
                            break
                    self.player_shooter1.attack_flg = 1
                    # self.snd_yeet.play()
                else:
                    for bullet in iter(self.bullets_r1):
                        if not bullet.live_flag:
                            bullet.rect.x = self.player_shooter1.rect.x
                            bullet.rect.y = self.player_shooter1.rect.y
                            bullet.live_flag = 1
                            break
                    self.player_shooter1.attack_flg = 1
                    # self.snd_yeet.play()

        # player_shooter0 controls
        if events_lst_shooter0[5] and self.player_shooter0.change_x < 0:
            self.player_shooter0.stop()
        if events_lst_shooter0[6] and self.player_shooter0.change_x > 0:
            self.player_shooter0.stop()

        # player_shooter1 controls
        if events_lst_shooter1[5] and self.player_shooter1.change_x < 0:
            self.player_shooter1.stop()
        if events_lst_shooter1[6] and self.player_shooter1.change_x > 0:
            self.player_shooter1.stop()

    def update(self):
        # Game Loop - Update
        # Update the player.
        self.active_sprite_grp.update()
        self.bullet_sprite_grp0.update()
        self.bullet_sprite_grp1.update()

        if self.player_shooter0.reload_timer > 0 and not self.r_sign_flg0:
            self.r_sign_flg0 = 1
        elif self.player_shooter0.reload_timer == 0 and self.r_sign_flg0:
            self.r_sign_flg0 = 0

        if self.player_shooter1.reload_timer > 0 and not self.r_sign_flg1:
            self.r_sign_flg1 = 1
        elif self.player_shooter1.reload_timer == 0 and self.r_sign_flg1:
            self.r_sign_flg1 = 0

        if self.player_shooter0 in self.active_sprite_grp:
            bullet_hit_shooter0 = pg.sprite.spritecollideany(self.player_shooter0, self.bullet_sprite_grp1)
            if bullet_hit_shooter0:
                bullet_hit_shooter0.live_flag = 0
                self.player_shooter0.hit_flag = 1
                self.player_shooter0.hit_count += 1

                if self.player_shooter0.hit_count == self.player_shooter0.hit_limit:
                    # self.active_sprite_grp.remove(self.player_shooter1)
                    self.match_score["shooter0"] += 1
                    # self.player_shooter1.hit_count = 0
                    self.winner, self.playing = self.check_winner()
                    if self.winner == "nobody":
                        # self.match_score["round"] += 1
                        self.new_round = True

            bullet_hit_shooter1 = pg.sprite.spritecollideany(self.player_shooter1, self.bullet_sprite_grp0)
            if bullet_hit_shooter1:
                bullet_hit_shooter1.live_flag = 0
                self.player_shooter1.hit_flag = 1
                self.player_shooter1.hit_count += 1

                if self.player_shooter1.hit_count == self.player_shooter1.hit_limit:
                    # self.active_sprite_grp.remove(self.player_shooter1)
                    self.match_score["shooter0"] += 1
                    # self.player_shooter1.hit_count = 0
                    self.winner, self.playing = self.check_winner()
                    if self.winner == "nobody":
                        # self.match_score["round"] += 1
                        self.new_round = True

        for i in range(TTL_BULLETS):
            if self.bullets_l0[i].live_flag == 0:
                self.bullets_l0[i].rect.x, self.bullets_l0[i].rect.y = DEAD_BULLET_POS
            if self.bullets_r0[i].live_flag == 0:
                self.bullets_r0[i].rect.x, self.bullets_r0[i].rect.y = DEAD_BULLET_POS
            if self.bullets_l1[i].live_flag == 0:
                self.bullets_l1[i].rect.x, self.bullets_l1[i].rect.y = DEAD_BULLET_POS
            if self.bullets_r1[i].live_flag == 0:
                self.bullets_r1[i].rect.x, self.bullets_r1[i].rect.y = DEAD_BULLET_POS
        # Update items in the level
        self.current_level.update()

    def check_winner(self):
        # return the winner role (if game over) or "nobody", and a bool value for self.playing
        self.match_score["match_type"] = MATCH_TYPE_LST[self.match_id]
        if self.match_score["match_type"] == MATCH_TYPE_LST[0]:
            # death match
            if self.match_score["shooter0"] == 1:
                return "shooter0", False
            elif self.match_score["shooter1"] == 1:
                return "shooter1", False
        elif self.match_score["match_type"] == MATCH_TYPE_LST[1]:
            # 1st23
            if self.match_score["shooter0"] == 3:
                return "shooter0", False
            elif self.match_score["shooter1"] == 3:
                return "shooter1", False
            else:
                return "nobody", True
        elif self.match_score["match_type"] == MATCH_TYPE_LST[2]:
            # best of 3
            if self.match_score["shooter0"] == 2:
                return "shooter0", False
            elif self.match_score["shooter1"] == 2:
                return "shooter1", False
            # elif self.match_score["shooter0"] == 3:
            #     return "shooter0", False
            # elif self.match_score["shooter1"] == 3:
            #     return "shooter1", False
            else:
                return "nobody", True


    def gs_conversion(self):
        game_state = []
        game_state.append(self.player_shooter0.img_dict_key)  # 0
        game_state.append(self.player_shooter0.image_idx)  # 1
        game_state.append((self.player_shooter0.rect.x, self.player_shooter0.rect.y))  # 2
        game_state.append(self.player_shooter1.img_dict_key)  # 3
        game_state.append(self.player_shooter1.image_idx)  # 4
        game_state.append((self.player_shooter1.rect.x, self.player_shooter1.rect.y))  # 5
        game_state.append((self.bullets_l0[0].rect.x, self.bullets_l0[0].rect.y))  # 6
        game_state.append((self.bullets_l0[1].rect.x, self.bullets_l0[1].rect.y))  # 7
        game_state.append((self.bullets_l0[2].rect.x, self.bullets_l0[2].rect.y))  # 8
        game_state.append((self.bullets_l0[3].rect.x, self.bullets_l0[3].rect.y))  # 9
        game_state.append((self.bullets_l0[4].rect.x, self.bullets_l0[4].rect.y))  # 10
        game_state.append((self.bullets_r0[0].rect.x, self.bullets_r0[0].rect.y))  # 11
        game_state.append((self.bullets_r0[1].rect.x, self.bullets_r0[1].rect.y))  # 12
        game_state.append((self.bullets_r0[2].rect.x, self.bullets_r0[2].rect.y))  # 13
        game_state.append((self.bullets_r0[3].rect.x, self.bullets_r0[3].rect.y))  # 14
        game_state.append((self.bullets_r0[4].rect.x, self.bullets_r0[4].rect.y))  # 15
        game_state.append((self.bullets_l1[0].rect.x, self.bullets_l1[0].rect.y))  # 16
        game_state.append((self.bullets_l1[1].rect.x, self.bullets_l1[1].rect.y))  # 17
        game_state.append((self.bullets_l1[2].rect.x, self.bullets_l1[2].rect.y))  # 18
        game_state.append((self.bullets_l1[3].rect.x, self.bullets_l1[3].rect.y))  # 19
        game_state.append((self.bullets_l1[4].rect.x, self.bullets_l1[4].rect.y))  # 20
        game_state.append((self.bullets_r1[0].rect.x, self.bullets_r1[0].rect.y))  # 21
        game_state.append((self.bullets_r1[1].rect.x, self.bullets_r1[1].rect.y))  # 22
        game_state.append((self.bullets_r1[2].rect.x, self.bullets_r1[2].rect.y))  # 23
        game_state.append((self.bullets_r1[3].rect.x, self.bullets_r1[3].rect.y))  # 24
        game_state.append((self.bullets_r1[4].rect.x, self.bullets_r1[4].rect.y))  # 25
        if self.current_level_no == 0:
            game_state.append(DEAD_CRATER_POS)  # 26
        else:
            game_state.append((self.level02.moving_block.rect.x, self.level02.moving_block.rect.y))  # 26
        game_state.append(self.r_sign_flg0)  # 27
        game_state.append(self.r_sign_flg1)  # 28
        game_state.append(self.map_id)  # 29
        game_state.append(self.match_id)  # 30
        game_state.append(self.current_level_no)  # 31
        game_state.append(self.match_score["round"])  # 32
        game_state.append(self.match_score["shooter0"])  # 33
        game_state.append(self.match_score["shooter1"])  # 34
        game_state.append(self.winner)  # 35
        game_state.append(self.player_shooter0.hit_count)  # 36
        game_state.append(self.player_shooter1.hit_count)  # 37

        return game_state


class GameCC:  # chopper vs chopper
    def __init__(self, screen, win_w, win_h, map_id, level_id, match_id):
        pg.init()
        # get settings when called by the server program
        self.screen = screen
        self.win_w = win_w
        self.win_h = win_h

        self.map_id = map_id
        # self.current_level_no = level_id
        self.current_level_no = map_id
        self.match_id = match_id
        self.new_round = False

        # match score
        self.match_score = {"match_type": MATCH_TYPE_LST[self.match_id],
                            "round": 1, "chopper0": 0, "chopper1": 0,
                            "map": MAP_LST[self.map_id], "game_finished": False}

        """
        0   , 1        , 2         , 3   , 4     , 5             , 6
        quit, move_left, move_right, jump, attack, move_left_stop, move_right_stop
        """
        self.events_str0 = "0000000"
        self.events_str1 = "0000000"
        self.events_lst0 = list(self.events_str0)
        self.events_lst1 = list(self.events_str1)
        # self.game_state = []

        self.current_level = None

        self.running = True

    def new(self):
        self.winner = "nobody"
        self.playing = True
        self.match_score = {"match_type": MATCH_TYPE_LST[self.match_id],
                            "round": 0, "chopper0": 0, "chopper1": 0,
                            "map": MAP_LST[self.map_id], "game_finished": False}

        # if self.match_score["game_finished"]:
        #     return
        # else:
        #     self.match_score["round"] += 1

        self.restart()

    def restart(self):
        # match type
        match_type = self.match_score["match_type"]

        # initialize variables
        self.match_score["round"] += 1

        # Create the self.player
        self.player_chopper0 = sprite_player_correction.Player()
        self.player_chopper0.hit_limit = CC_CHOPPER_SCORE_HIT

        self.player_chopper1 = sprite_player_correction.Player()
        self.player_chopper1.hit_limit = CC_CHOPPER_SCORE_HIT
        
        self.role_lst = [self.player_chopper0, self.player_chopper1]

        # Create all the levels
        self.level_list = []
        self.level01 = Level_01(self.player_chopper0, self.player_chopper1)
        self.level02 = Level_02(self.player_chopper0, self.player_chopper1)
        self.level_list.append(self.level01)
        self.level_list.append(self.level02)

        # Set the current level
        self.current_level = self.level_list[self.current_level_no]

        self.active_sprite_grp = pg.sprite.Group()

        self.player_chopper0.level = self.current_level
        self.player_chopper0.rect.x = 200
        self.player_chopper0.rect.y = -50
        
        self.player_chopper1.level = self.current_level
        self.player_chopper1.rect.x = 700
        self.player_chopper1.rect.y = -50

        self.active_sprite_grp.add(self.player_chopper0, self.player_chopper1)

    def events(self):
        # Game Loop - events
        # lst_s = list(self.events_str_shooter)
        # lst_c = list(self.events_str_chopper)

        events_lst_chopper0 = [int(item) for item in self.events_lst0]
        events_lst_chopper1 = [int(item) for item in self.events_lst1]

        if events_lst_chopper0[0] or events_lst_chopper1[0]:
            if self.playing:
                self.playing = False
            self.running = False

        # player_chopper0 controls
        if events_lst_chopper0[1]:
            self.player_chopper0.go_left()
        if events_lst_chopper0[2]:
            self.player_chopper0.go_right()
        if events_lst_chopper0[3]:
            self.player_chopper0.jump()
        if events_lst_chopper0[4]:
            self.player_chopper0.chop()
            self.player_chopper0.image_idx = 0

        if events_lst_chopper0[5] and self.player_chopper0.change_x < 0:
            self.player_chopper0.stop()
        if events_lst_chopper0[6] and self.player_chopper0.change_x > 0:
            self.player_chopper0.stop()
        
        # player_chopper1 controls
        if events_lst_chopper1[1]:
            self.player_chopper1.go_left()
        if events_lst_chopper1[2]:
            self.player_chopper1.go_right()
        if events_lst_chopper1[3]:
            self.player_chopper1.jump()
        if events_lst_chopper1[4]:
            self.player_chopper1.chop()
            self.player_chopper1.image_idx = 0

        if events_lst_chopper1[5] and self.player_chopper1.change_x < 0:
            self.player_chopper1.stop()
        if events_lst_chopper1[6] and self.player_chopper1.change_x > 0:
            self.player_chopper1.stop()

    def update(self):
        # Game Loop - Update
        # Update the player.
        self.active_sprite_grp.update()

        if pg.sprite.collide_rect(self.player_chopper0, self.player_chopper1):
            if self.player_chopper0.hit_flag == 0 and self.player_chopper1.chop_flag == 1:
                self.player_chopper0.hit_flag = 1
                self.player_chopper0.hit_count += 1
                if self.player_chopper0.hit_count == self.player_chopper0.hit_limit:
                    self.match_score["chopper1"] += 1
                    self.winner, self.playing = self.check_winner()
                    if self.winner == "nobody":
                        self.new_round = True
            elif self.player_chopper0.hit_flag == 1 and self.player_chopper1.chop_flag == 0:
                self.player_chopper0.hit_flag = 0
            
            if self.player_chopper1.hit_flag == 0 and self.player_chopper0.chop_flag == 1:
                self.player_chopper1.hit_flag = 1
                self.player_chopper1.hit_count += 1
                if self.player_chopper1.hit_count == self.player_chopper1.hit_limit:
                    self.match_score["chopper0"] += 1
                    self.winner, self.playing = self.check_winner()
                    if self.winner == "nobody":
                        self.new_round = True
            elif self.player_chopper1.hit_flag == 1 and self.player_chopper0.chop_flag == 0:
                self.player_chopper1.hit_flag = 0
            
        # Update items in the level
        self.current_level.update()

    def check_winner(self):
        # return the winner role (if game over) or "nobody", and a bool value for self.playing
        self.match_score["match_type"] = MATCH_TYPE_LST[self.match_id]
        if self.match_score["match_type"] == MATCH_TYPE_LST[0]:
            # death match
            if self.match_score["chopper0"] == 1:
                return "chopper0", False
            elif self.match_score["chopper1"] == 1:
                return "chopper1", False
        elif self.match_score["match_type"] == MATCH_TYPE_LST[1]:
            # 1st23
            if self.match_score["chopper0"] == 3:
                return "chopper0", False
            elif self.match_score["chopper1"] == 3:
                return "chopper1", False
            else:
                return "nobody", True
        elif self.match_score["match_type"] == MATCH_TYPE_LST[2]:
            # best of 3
            if self.match_score["chopper0"] == 2:
                return "chopper0", False
            elif self.match_score["chopper1"] == 2:
                return "chopper1", False
            else:
                return "nobody", True

    def gs_conversion(self):
        game_state = []
        game_state.append(self.player_chopper0.img_dict_key)  # 0
        game_state.append(self.player_chopper0.image_idx)  # 1
        game_state.append((self.player_chopper0.rect.x, self.player_chopper0.rect.y))  # 2
        game_state.append(self.player_chopper1.img_dict_key)  # 3
        game_state.append(self.player_chopper1.image_idx)  # 4
        game_state.append((self.player_chopper1.rect.x, self.player_chopper1.rect.y))  # 5
        if self.current_level_no == 0:
            game_state.append(DEAD_CRATER_POS)  # 6
        else:
            game_state.append((self.level02.moving_block.rect.x, self.level02.moving_block.rect.y))  # 6
        game_state.append(self.map_id)  # 7
        game_state.append(self.match_id)  # 8
        game_state.append(self.current_level_no)  # 9
        game_state.append(self.match_score["round"])  # 10
        game_state.append(self.match_score["chopper0"])  # 11
        game_state.append(self.match_score["chopper1"])  # 12
        game_state.append(self.winner)  # 13
        game_state.append(self.player_chopper0.hit_count)  # 14
        game_state.append(self.player_chopper1.hit_count)  # 15

        return game_state


"""
game type selection:

player0_role_id = 0, player1_role_id = 0, player0_role_id + player1_role_id = 0, both players are shooters, GameSS 
player0_role_id or player1_role_id = 1, player0_role_id + player1_role_id = 1, one shooter one chopper, GameSC 
player0_role_id = 1, player1_role_id = 1, player0_role_id + player1_role_id = 2, both players are choppers, GameCC 
"""
game_type_lst = [GameSS, GameSC, GameCC]