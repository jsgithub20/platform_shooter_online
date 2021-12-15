import pygame as pg
from sys import exit
from platform_shooter_settings import *
from platform_shooter_sprites import *
import sprite_player_correction
from role_def import *


class Game:
    def __init__(self, screen, win_w, win_h, map_id, level_id, match_id, player0_id, player1_id):
        pg.init()
        # get settings when called by the server program
        self.screen = screen
        self.win_w = win_w
        self.win_h = win_h

        self.map_id = map_id
        self.current_level_no = level_id
        self.match_id = match_id

        # match types
        self.match_types = ["Deathmatch", "1st23", "Best of 3"]

        # match score
        self.match_score = {"match_type": self.match_types[self.match_id],
                            "round": 0, "shooter": 0, "chopper": 0,
                            "map": 0, "game_finished": False}

        # player selection
        self.player_lst = []  # player sprites
        self.player0_id = player0_id
        self.player1_id = player1_id

        # the "R" sign on the shooter's head to indicate it's the reloading time, so it can't shoot
        self.r_sign = False
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
        self.bullets = []

        # Create the self.player
        self.player_shooter = Player()
        self.player_shooter.hit_limit = 3

        self.player_chopper = sprite_player_correction.Player()
        self.player_chopper.hit_limit = 3

        self.player_lst.append(self.player_shooter)
        self.player_lst.append(self.player_chopper)

        # Create all the levels
        self.level_list = []
        self.level_list.append(Level_01(self.player_shooter, self.player_chopper))
        self.level_list.append(Level_02(self.player_shooter, self.player_chopper))

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
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    self.mouse_pos_flag = not self.mouse_pos_flag
                    if self.mouse_pos_flag:
                        self.active_sprite_list.add(self.mouse_pos)
                    else:
                        self.active_sprite_list.remove(self.mouse_pos)
                # player_shooter controls
                if event.key == pg.K_LEFT:
                    self.player_shooter.go_left()
                if event.key == pg.K_RIGHT:
                    self.player_shooter.go_right()
                if event.key == pg.K_UP:
                    self.player_shooter.jump()
                if event.key == pg.K_SPACE:
                    if self.player_shooter.loaded > 0:
                        self.player_shooter.image_idx = 0
                        self.player_shooter.loaded -= 1
                        if self.player_shooter.direction == 'l':
                            bullet = Bullet(self.player_shooter.rect.x, self.player_shooter.rect.y, 'l', SCREEN_WIDTH)
                            bullet.level = self.current_level
                            self.player_shooter.attack_flg = 1
                            self.snd_yeet.play()
                        else:
                            bullet = Bullet(self.player_shooter.rect.x, self.player_shooter.rect.y, 'r', SCREEN_WIDTH)
                            bullet.level = self.current_level
                            self.player_shooter.attack_flg = 1
                            self.snd_yeet.play()
                        self.bullets.append(bullet)
                        self.bullet_sprite_grp.add(bullet)

                # player_chopper controls
                if event.key == pg.K_a:
                    self.player_chopper.go_left()
                elif event.key == pg.K_d:
                    self.player_chopper.go_right()
                if event.key == pg.K_w:
                    self.player_chopper.jump()
                if event.key == pg.K_c:
                    self.player_chopper.chop()
                    self.player_chopper.image_idx = 0

            if event.type == pg.KEYUP:
                # player_shooter controls
                if event.key == pg.K_LEFT and self.player_shooter.change_x < 0:
                    self.player_shooter.stop()
                if event.key == pg.K_RIGHT and self.player_shooter.change_x > 0:
                    self.player_shooter.stop()

                # player_chopper controls
                if event.key == pg.K_a and self.player_chopper.change_x < 0:
                    self.player_chopper.stop()
                if event.key == pg.K_d and self.player_chopper.change_x > 0:
                    self.player_chopper.stop()

    def update(self):
        # Game Loop - Update
        # Update the player.
        self.active_sprite_list.update()
        self.bullet_sprite_grp.update()

        if self.mouse_pos in self.active_sprite_list:
            self.mouse_pos.text = f"({str(pg.mouse.get_pos()[0])},{str(pg.mouse.get_pos()[1])})"

        # Update the r_sign to follow the player_shooter
        self.r_sign.rect.midbottom = self.player_shooter.rect.midtop
        if self.player_shooter.reload_timer > 0 and self.r_sign not in self.active_sprite_list:
            self.active_sprite_list.add(self.r_sign)
        elif self.player_shooter.reload_timer == 0 and self.r_sign in self.active_sprite_list:
            self.active_sprite_list.remove(self.r_sign)

        if self.player_chopper in self.active_sprite_list:
            bullet_hit_chopper = pg.sprite.spritecollideany(self.player_chopper, self.bullet_sprite_grp)
            if bullet_hit_chopper:
                bullet_hit_chopper.live_flag = 0
                self.player_chopper.hit_flag = 1
                self.player_chopper.hit_count += 1

                if self.player_chopper.hit_count == self.player_chopper.hit_limit:
                    # self.active_sprite_list.remove(self.player_chopper)
                    self.match_score["shooter"] += 1
                    self.winner, self.playing = self.check_winner()
                    if self.winner is None:
                        self.restart()

            if pg.sprite.collide_rect(self.player_shooter, self.player_chopper):
                if self.player_shooter.hit_flag == 0 and self.player_chopper.chop_flag == 1:
                    self.player_shooter.hit_flag = 1
                    self.player_shooter.hit_count += 1
                    if self.player_shooter.hit_count >= self.player_shooter.hit_limit:
                        # self.active_sprite_list.remove(self.player_shooter)
                        self.match_score["chopper"] += 1
                        self.winner, self.playing = self.check_winner()
                        if self.winner is None:
                            self.restart()

                elif self.player_shooter.hit_flag == 1 and self.player_chopper.chop_flag == 0:
                    self.player_shooter.hit_flag = 0

        if self.bullets:
            for bullet in self.bullets:
                if bullet.live_flag == 0:
                    self.bullet_sprite_grp.remove(bullet)
                    self.bullets.remove(bullet)

        # Update items in the level
        self.current_level.update()

        self.fps_txt.text = f"fps: {str(int(self.clock.get_fps()))}"
        self.player_shooter_score.text = "Shooter Hit: {}/{}".format(self.player_shooter.hit_count,
                                                                     self.player_shooter.hit_limit)
        self.player_chopper_score.text = "Chopper Hit: {}/{}".format(self.player_chopper.hit_count,
                                                                     self.player_chopper.hit_limit)

    def check_winner(self):
        # return the winner role (if game over) or None, and a bool value for self.playing
        if self.match_score["match_type"] == self.match_types[0]:
            # death match
            if self.match_score["shooter"] == 1:
                return "shooter", False
            elif self.match_score["chopper"] == 1:
                return "chopper", False
        elif self.match_score["match_type"] == self.match_types[1]:
            # 1st23
            if self.match_score["shooter"] == 3:
                return "shooter", False
            elif self.match_score["chopper"] == 3:
                return "chopper", False
            else:
                return None, True
        elif self.match_score["match_type"] == self.match_types[2]:
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
