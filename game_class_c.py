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


running = True


class GameSC:
    def __init__(self, screen, win_w, win_h, map_id, match_id, player_id, role_id, my_name, your_name):
        pg.init()
        self.clock = pg.time.Clock()
        self.timer = pg.time.get_ticks()
        self.screen = screen
        self.win_w = win_w
        self.win_h = win_h
        self.splat_font = ft.Font("resources/fonts/earwig factory rg.ttf", 60)
        self.counting_font = ft.Font("resources/OvOV20.ttf", 60)
        self.counting = 3

        self.map_id = map_id
        # self.current_level_no = 0
        self.current_level_no = map_id
        self.match_id = match_id
        self.player_id = player_id
        self.role_id = role_id
        self.round = 0
        self.round_count_down_flag = False
        self.my_name = my_name
        self.your_name = your_name
        self.role_lst = ["shooter", "chopper"]

        """
        0   , 1        , 2         , 3   , 4     , 5             , 6
        quit, move_left, move_right, jump, attack, move_left_stop, move_right_stop
        """

        self.events_str = "0000000"
        self.events_lst = ["0", "0", "0", "0", "0", "0", "0"]

        self.current_level = None

        self.snd_yeet = pg.mixer.Sound("resources/sound/yeet.ogg")
        self.snd_yeet.set_volume(0.2)

        # self.running = True

    def new(self):
        self.winner = None
        self.playing = True
        self.round = 0

        pg.mixer.music.load("resources/sound/Resurrection of the Dagger.ogg")
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(loops=-1)

        self.bullets_l = []
        self.live_bullet_l = 0
        for i in range(TTL_BULLETS):
            bullet = Bullet(DEAD_BULLET_POS, 'l', SCREEN_WIDTH)
            # bullet.level = self.current_level
            self.bullets_l.append(bullet)

        self.bullets_r = []
        self.live_bullet_r = 0
        for i in range(TTL_BULLETS):
            bullet = Bullet(DEAD_BULLET_POS, 'r', SCREEN_WIDTH)
            # bullet.level = self.current_level
            self.bullets_r.append(bullet)

        # the "R" sign on the shooter's head to indicate it's the reloading time, so it can't shoot
        self.r_sign = DrawText(self.screen, 30, RED, 0, 0, "r_sign", "R", 0, 10)

        self.fps_txt = DrawText(self.screen, 20, LIGHT_GREEN, 5, 5, "fps_txt", "0")

        self.shooter_score = "0"
        self.chopper_score = "0"

        match_score = f"{self.shooter_score} - {MATCH_TYPE_LST[self.match_id]} - {self.chopper_score}"
        self.level_txt = DrawText(self.screen, 30, WHITE, 20, 10, "level", f"Level {self.current_level_no}", alignment="center")
        self.match_type_txt = DrawText(self.screen, 30, WHITE, 25, 720, "match_score", match_score, alignment="center")

        if self.player_id == 0:
            self.my_name_txt = DrawText(self.screen, 30, WHITE, 25, 720, "my_name", self.my_name, alignment="left")
            self.your_name_txt = DrawText(self.screen, 30, WHITE, 25, 720, "your_name", self.your_name, alignment="right")
            self.my_health_bar = HealthBar(10, 750, SHOOTER_SCORE_HIT)
            self.your_health_bar = HealthBar(820, 750, CHOPPER_SCORE_HIT)
        elif self.player_id == 1:
            self.my_name_txt = DrawText(self.screen, 30, WHITE, 25, 720, "my_name", self.my_name, alignment="right")
            self.your_name_txt = DrawText(self.screen, 30, WHITE, 25, 720, "your_name", self.your_name, alignment="left")
            self.your_health_bar = HealthBar(10, 750, SHOOTER_SCORE_HIT)
            self.my_health_bar = HealthBar(810, 750, CHOPPER_SCORE_HIT)

        self.restart()

    def restart(self):
        # start a new game
        self.player_shooter = Player()
        self.player_chopper = sprite_player_correction.Player()

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

        self.player_chopper.level = self.current_level

        self.active_sprite_grp.add(self.player_shooter, self.player_chopper, self.r_sign)
        self.upd_text_sprite_grp.add(self.fps_txt, self.match_type_txt, self.my_health_bar, self.your_health_bar)  # only text sprites that need to be updated
        self.idle_text_sprite_grp.add(self.my_name_txt, self.your_name_txt, self.level_txt)
        self.bullet_sprite_grp.add(*self.bullets_r, *self.bullets_l)

    def events(self):
        # Game Loop - events
        for i in range(len(self.events_lst)):
            self.events_lst[i] = "0"
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.events_lst[0] = QUIT
                self.playing = False
                global running
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.events_lst[0] = QUIT
                    self.playing = False
                    # global running
                    running = False
                # player_shooter controls
                if event.key == pg.K_LEFT:
                    self.events_lst[1] = "1"
                if event.key == pg.K_RIGHT:
                    self.events_lst[2] = "1"
                if event.key == pg.K_UP:
                    self.events_lst[3] = "1"
                if event.key == pg.K_SPACE:
                    if self.role_lst[self.role_id] == "chopper":
                        if (pg.time.get_ticks() - self.timer) > CHOPPER_CD:
                            self.events_lst[4] = "1"
                            self.timer = pg.time.get_ticks()
                    else:
                        self.events_lst[4] = "1"
                        self.snd_yeet.play()

            if event.type == pg.KEYUP:
                # player_shooter controls
                if event.key == pg.K_LEFT:
                    self.events_lst[5] = "1"
                if event.key == pg.K_RIGHT:
                    self.events_lst[6] = "1"

        if self.round_count_down_flag and self.counting >= 0:
            self.events_lst[0] = HOLD
            if pg.time.get_ticks() - self.timer >= 1000 and self.counting > 0:
                self.counting -= 1
                self.timer = pg.time.get_ticks()
            elif pg.time.get_ticks() - self.timer >= 1000 and self.counting == 0:
                self.round_count_down_flag = False
        else:
            self.round_count_down_flag = False

        self.events_str = "".join(self.events_lst)

    def update_game_state(self, gs_lst):
        self.clock.tick()
        if gs_lst[21] > self.round:
            self.round = gs_lst[21]
            self.round_count_down_flag = True
            self.counting = 3
            self.timer = pg.time.get_ticks()
        if gs_lst[24] != "nobody":
            self.winner = gs_lst[24]
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

        self.match_type_txt.text = f"{gs_lst[22]} - {MATCH_TYPE_LST[int(gs_lst[19])]} - {gs_lst[23]}"
        self.fps_txt.text = str(int(self.clock.get_fps()))
        if self.player_id == 0:
            self.my_health_bar.hit = gs_lst[25]
            self.your_health_bar.hit = gs_lst[26]
        elif self.player_id == 1:
            self.my_health_bar.hit = gs_lst[26]
            self.your_health_bar.hit = gs_lst[25]
        self.upd_text_sprite_grp.update()

    def draw(self):
        self.current_level.draw(self.screen)
        self.active_sprite_grp.draw(self.screen)
        self.bullet_sprite_grp.draw(self.screen)
        self.upd_text_sprite_grp.draw(self.screen)
        self.idle_text_sprite_grp.draw(self.screen)
        if self.round_count_down_flag:
            self.counting_font.render_to(self.screen, (400, 200), f"ROUND {self.round}",
                                         fgcolor=RED, bgcolor=GREEN)
            self.counting_font.render_to(self.screen, (500, 300), f"{self.counting}",
                                         fgcolor=RED, bgcolor=GREEN)

        pg.display.update()


class GameSS:
    def __init__(self, screen, win_w, win_h, map_id, match_id, player_id, role_id, my_name, your_name):
        pg.init()
        self.clock = pg.time.Clock()
        self.timer = pg.time.get_ticks()
        self.screen = screen
        self.win_w = win_w
        self.win_h = win_h
        self.splat_font = ft.Font("resources/fonts/earwig factory rg.ttf", 60)
        self.counting_font = ft.Font("resources/OvOV20.ttf", 60)
        self.counting = 3

        self.map_id = map_id
        # self.current_level_no = 0
        self.current_level_no = map_id
        self.match_id = match_id
        self.player_id = player_id
        self.role_id = role_id
        self.round = 0
        self.round_count_down_flag = False
        self.my_name = my_name
        self.your_name = your_name
        self.role_lst = ["shooter", "shooter1"]

        """
        0   , 1        , 2         , 3   , 4     , 5             , 6
        quit, move_left, move_right, jump, attack, move_left_stop, move_right_stop
        """

        self.events_str = "0000000"
        self.events_lst = ["0", "0", "0", "0", "0", "0", "0"]

        self.current_level = None

        self.snd_yeet = pg.mixer.Sound("resources/sound/yeet.ogg")
        self.snd_yeet.set_volume(0.2)

        # self.running = True

    def new(self):
        self.winner = None
        self.playing = True
        self.round = 0

        pg.mixer.music.load("resources/sound/Resurrection of the Dagger.ogg")
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(loops=-1)

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
        self.r_sign0 = DrawText(self.screen, 30, RED, 0, 0, "r_sign0", "R", 0, 10)
        self.r_sign1 = DrawText(self.screen, 30, RED, 0, 0, "r_sign", "R", 0, 10)

        self.fps_txt = DrawText(self.screen, 20, LIGHT_GREEN, 5, 5, "fps_txt", "0")

        self.shooter0_score = "0"
        self.shooter1_score = "0"

        match_score = f"{self.shooter0_score} - {MATCH_TYPE_LST[self.match_id]} - {self.shooter1_score}"
        self.level_txt = DrawText(self.screen, 30, WHITE, 20, 10, "level", f"Level {self.current_level_no}", alignment="center")
        self.match_type_txt = DrawText(self.screen, 30, WHITE, 25, 720, "match_score", match_score, alignment="center")

        if self.player_id == 0:
            self.my_name_txt = DrawText(self.screen, 30, WHITE, 25, 720, "my_name", self.my_name, alignment="left")
            self.your_name_txt = DrawText(self.screen, 30, WHITE, 25, 720, "your_name", self.your_name, alignment="right")
            self.my_health_bar = HealthBar(10, 750, SS_SHOOTER_SCORE_HIT)
            self.your_health_bar = HealthBar(820, 750, SS_SHOOTER_SCORE_HIT)
        elif self.player_id == 1:
            self.my_name_txt = DrawText(self.screen, 30, WHITE, 25, 720, "my_name", self.my_name, alignment="right")
            self.your_name_txt = DrawText(self.screen, 30, WHITE, 25, 720, "your_name", self.your_name, alignment="left")
            self.your_health_bar = HealthBar(10, 750, SS_SHOOTER_SCORE_HIT)
            self.my_health_bar = HealthBar(810, 750, SS_SHOOTER_SCORE_HIT)

        self.restart()

    def restart(self):
        # start a new game
        if self.player_id == 0:
            self.player_shooter0 = Player(0)
            self.player_shooter1 = Player(1)
        elif self.player_id == 1:
            self.player_shooter0 = Player(1)
            self.player_shooter1 = Player(0)

        # Create all the levels
        self.level_list = []
        self.level01 = Level_01(self.player_shooter0, self.player_shooter1)
        self.level02 = Level_02(self.player_shooter0, self.player_shooter1)
        self.level_list.append(self.level01)
        self.level_list.append(self.level02)

        # Set the current level
        self.current_level = self.level_list[self.current_level_no]
        self.level_txt.text = f"Level {self.current_level_no}"

        self.active_sprite_grp = pg.sprite.Group()
        self.bullet_sprite_grp0 = pg.sprite.Group()
        self.bullet_sprite_grp1 = pg.sprite.Group()
        self.upd_text_sprite_grp = pg.sprite.Group()
        self.idle_text_sprite_grp = pg.sprite.Group()

        self.player_shooter0.level = self.current_level

        self.player_shooter1.level = self.current_level

        self.active_sprite_grp.add(self.player_shooter0, self.player_shooter1, self.r_sign0, self.r_sign1)
        self.upd_text_sprite_grp.add(self.fps_txt, self.match_type_txt, self.my_health_bar, self.your_health_bar)  # only text sprites that need to be updated
        self.idle_text_sprite_grp.add(self.my_name_txt, self.your_name_txt, self.level_txt)
        self.bullet_sprite_grp0.add(*self.bullets_r0, *self.bullets_l0)
        self.bullet_sprite_grp1.add(*self.bullets_r1, *self.bullets_l1)

    def events(self):
        # Game Loop - events
        for i in range(len(self.events_lst)):
            self.events_lst[i] = "0"
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.events_lst[0] = QUIT
                self.playing = False
                global running
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.events_lst[0] = QUIT
                    self.playing = False
                    # global running
                    running = False
                # player_shooter controls
                if event.key == pg.K_LEFT:
                    self.events_lst[1] = "1"
                if event.key == pg.K_RIGHT:
                    self.events_lst[2] = "1"
                if event.key == pg.K_UP:
                    self.events_lst[3] = "1"
                if event.key == pg.K_SPACE:
                    self.events_lst[4] = "1"
                    self.snd_yeet.play()

            if event.type == pg.KEYUP:
                # player_shooter controls
                if event.key == pg.K_LEFT:
                    self.events_lst[5] = "1"
                if event.key == pg.K_RIGHT:
                    self.events_lst[6] = "1"

        if self.round_count_down_flag and self.counting >= 0:
            self.events_lst[0] = HOLD
            if pg.time.get_ticks() - self.timer >= 1000 and self.counting > 0:
                self.counting -= 1
                self.timer = pg.time.get_ticks()
            elif pg.time.get_ticks() - self.timer >= 1000 and self.counting == 0:
                self.round_count_down_flag = False
        else:
            self.round_count_down_flag = False

        self.events_str = "".join(self.events_lst)

    def update_game_state(self, gs_lst):
        self.clock.tick()
        if gs_lst[32] > self.round:
            self.round = gs_lst[32]
            self.round_count_down_flag = True
            self.counting = 3
            self.timer = pg.time.get_ticks()
        if gs_lst[35] != "nobody":
            self.winner = gs_lst[35]
            self.playing = False
        self.player_shooter0.update_img(gs_lst[0], gs_lst[1])
        self.player_shooter0.rect.x, self.player_shooter0.rect.y = gs_lst[2]
        self.player_shooter1.update_img(gs_lst[3], gs_lst[4])
        self.player_shooter1.rect.x, self.player_shooter1.rect.y = gs_lst[5]
        for i in range(TTL_BULLETS):
            self.bullets_l0[i].rect.x, self.bullets_l0[i].rect.y = gs_lst[i+6]
            self.bullets_r0[i].rect.x, self.bullets_r0[i].rect.y = gs_lst[i+11]
            self.bullets_l1[i].rect.x, self.bullets_l1[i].rect.y = gs_lst[i+16]
            self.bullets_r1[i].rect.x, self.bullets_r1[i].rect.y = gs_lst[i+21]
        if self.current_level_no == 1:
            self.current_level.moving_block.rect.x, self.current_level.moving_block.rect.y = gs_lst[26]
        if gs_lst[27]:  # r_sign_flg = 1
            self.r_sign0.rect.midbottom = self.player_shooter0.rect.midtop
        else:  # r_sign_flg = 0
            self.r_sign0.rect.midbottom = (-99, -99)
        if gs_lst[28]:  # r_sign_flg = 1
            self.r_sign1.rect.midbottom = self.player_shooter1.rect.midtop
        else:  # r_sign_flg = 0
            self.r_sign1.rect.midbottom = (-99, -99)

        self.match_type_txt.text = f"{gs_lst[33]} - {MATCH_TYPE_LST[int(gs_lst[30])]} - {gs_lst[34]}"
        self.fps_txt.text = str(int(self.clock.get_fps()))
        if self.player_id == 0:
            self.my_health_bar.hit = gs_lst[36]
            self.your_health_bar.hit = gs_lst[37]
        elif self.player_id == 1:
            self.my_health_bar.hit = gs_lst[37]
            self.your_health_bar.hit = gs_lst[36]
        self.upd_text_sprite_grp.update()

    def draw(self):
        self.current_level.draw(self.screen)
        self.active_sprite_grp.draw(self.screen)
        self.bullet_sprite_grp0.draw(self.screen)
        self.bullet_sprite_grp1.draw(self.screen)
        self.upd_text_sprite_grp.draw(self.screen)
        self.idle_text_sprite_grp.draw(self.screen)
        if self.round_count_down_flag:
            self.counting_font.render_to(self.screen, (400, 200), f"ROUND {self.round}",
                                         fgcolor=RED, bgcolor=GREEN)
            self.counting_font.render_to(self.screen, (500, 300), f"{self.counting}",
                                         fgcolor=RED, bgcolor=GREEN)

        pg.display.update()


class GameCC:
    def __init__(self, screen, win_w, win_h, map_id, match_id, player_id, role_id, my_name, your_name):
        pg.init()
        self.clock = pg.time.Clock()
        self.timer = pg.time.get_ticks()
        self.screen = screen
        self.win_w = win_w
        self.win_h = win_h
        self.splat_font = ft.Font("resources/fonts/earwig factory rg.ttf", 60)
        self.counting_font = ft.Font("resources/OvOV20.ttf", 60)
        self.counting = 3

        self.map_id = map_id
        # self.current_level_no = 0
        self.current_level_no = map_id
        self.match_id = match_id
        self.player_id = player_id
        self.role_id = role_id
        self.round = 0
        self.round_count_down_flag = False
        self.my_name = my_name
        self.your_name = your_name
        self.role_lst = ["chopper0", "chopper1"]

        """
        0   , 1        , 2         , 3   , 4     , 5             , 6
        quit, move_left, move_right, jump, attack, move_left_stop, move_right_stop
        """

        self.events_str = "0000000"
        self.events_lst = ["0", "0", "0", "0", "0", "0", "0"]

        self.current_level = None

        # self.running = True

    def new(self):
        self.winner = None
        self.playing = True
        self.round = 0

        pg.mixer.music.load("resources/sound/Resurrection of the Dagger.ogg")
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(loops=-1)

        self.fps_txt = DrawText(self.screen, 20, LIGHT_GREEN, 5, 5, "fps_txt", "0")

        self.chopper0_score = "0"
        self.chopper1_score = "0"

        match_score = f"{self.chopper0_score} - {MATCH_TYPE_LST[self.match_id]} - {self.chopper1_score}"
        self.level_txt = DrawText(self.screen, 30, WHITE, 20, 10, "level", f"Level {self.current_level_no}",
                                  alignment="center")
        self.match_type_txt = DrawText(self.screen, 30, WHITE, 25, 720, "match_score", match_score, alignment="center")

        if self.player_id == 0:
            self.my_name_txt = DrawText(self.screen, 30, WHITE, 25, 720, "my_name", self.my_name, alignment="left")
            self.your_name_txt = DrawText(self.screen, 30, WHITE, 25, 720, "your_name", self.your_name,
                                          alignment="right")
            self.my_health_bar = HealthBar(10, 750, CC_CHOPPER_SCORE_HIT)
            self.your_health_bar = HealthBar(820, 750, CC_CHOPPER_SCORE_HIT)
        elif self.player_id == 1:
            self.my_name_txt = DrawText(self.screen, 30, WHITE, 25, 720, "my_name", self.my_name, alignment="right")
            self.your_name_txt = DrawText(self.screen, 30, WHITE, 25, 720, "your_name", self.your_name,
                                          alignment="left")
            self.your_health_bar = HealthBar(10, 750, CC_CHOPPER_SCORE_HIT)
            self.my_health_bar = HealthBar(810, 750, CC_CHOPPER_SCORE_HIT)

        self.restart()

    def restart(self):
        # start a new game
        if self.player_id == 0:
            self.player_chopper0 = sprite_player_correction.Player(0)
            self.player_chopper1 = sprite_player_correction.Player(1)
        elif self.player_id == 1:
            self.player_chopper0 = sprite_player_correction.Player(1)
            self.player_chopper1 = sprite_player_correction.Player(0)

        # Create all the levels
        self.level_list = []
        self.level01 = Level_01(self.player_chopper0, self.player_chopper1)
        self.level02 = Level_02(self.player_chopper0, self.player_chopper1)
        self.level_list.append(self.level01)
        self.level_list.append(self.level02)

        # Set the current level
        self.current_level = self.level_list[self.current_level_no]
        self.level_txt.text = f"Level {self.current_level_no}"

        self.active_sprite_grp = pg.sprite.Group()
        self.bullet_sprite_grp = pg.sprite.Group()
        self.upd_text_sprite_grp = pg.sprite.Group()
        self.idle_text_sprite_grp = pg.sprite.Group()

        self.player_chopper0.level = self.current_level

        self.player_chopper1.level = self.current_level

        self.active_sprite_grp.add(self.player_chopper0, self.player_chopper1)
        self.upd_text_sprite_grp.add(self.fps_txt, self.match_type_txt, self.my_health_bar,
                                     self.your_health_bar)  # only text sprites that need to be updated
        self.idle_text_sprite_grp.add(self.my_name_txt, self.your_name_txt, self.level_txt)

    def events(self):
        # Game Loop - events
        for i in range(len(self.events_lst)):
            self.events_lst[i] = "0"
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.events_lst[0] = QUIT
                self.playing = False
                global running
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.events_lst[0] = QUIT
                    self.playing = False
                    # global running
                    running = False
                if event.key == pg.K_LEFT:
                    self.events_lst[1] = "1"
                if event.key == pg.K_RIGHT:
                    self.events_lst[2] = "1"
                if event.key == pg.K_UP:
                    self.events_lst[3] = "1"
                if event.key == pg.K_SPACE:
                    if (pg.time.get_ticks() - self.timer) > CHOPPER_CD:
                        self.events_lst[4] = "1"
                        self.timer = pg.time.get_ticks()

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    self.events_lst[5] = "1"
                if event.key == pg.K_RIGHT:
                    self.events_lst[6] = "1"

        if self.round_count_down_flag and self.counting >= 0:
            self.events_lst[0] = HOLD
            if pg.time.get_ticks() - self.timer >= 1000 and self.counting > 0:
                self.counting -= 1
                self.timer = pg.time.get_ticks()
            elif pg.time.get_ticks() - self.timer >= 1000 and self.counting == 0:
                self.round_count_down_flag = False
        else:
            self.round_count_down_flag = False

        self.events_str = "".join(self.events_lst)

    def update_game_state(self, gs_lst):
        self.clock.tick()
        if gs_lst[10] > self.round:
            self.round = gs_lst[10]
            self.round_count_down_flag = True
            self.counting = 3
            self.timer = pg.time.get_ticks()
        if gs_lst[13] != "nobody":
            self.winner = gs_lst[13]
            self.playing = False
        self.player_chopper0.update_img(gs_lst[0], gs_lst[1])
        self.player_chopper0.rect.x, self.player_chopper0.rect.y = gs_lst[2]
        self.player_chopper1.update_img(gs_lst[3], gs_lst[4])
        self.player_chopper1.rect.x, self.player_chopper1.rect.y = gs_lst[5]
        if self.current_level_no == 1:
            self.current_level.moving_block.rect.x, self.current_level.moving_block.rect.y = gs_lst[6]

        self.match_type_txt.text = f"{gs_lst[11]} - {MATCH_TYPE_LST[int(gs_lst[8])]} - {gs_lst[12]}"
        self.fps_txt.text = str(int(self.clock.get_fps()))
        if self.player_id == 0:
            self.my_health_bar.hit = gs_lst[14]
            self.your_health_bar.hit = gs_lst[15]
        elif self.player_id == 1:
            self.my_health_bar.hit = gs_lst[15]
            self.your_health_bar.hit = gs_lst[14]
        self.upd_text_sprite_grp.update()

    def draw(self):
        self.current_level.draw(self.screen)
        self.active_sprite_grp.draw(self.screen)
        self.upd_text_sprite_grp.draw(self.screen)
        self.idle_text_sprite_grp.draw(self.screen)
        if self.round_count_down_flag:
            self.counting_font.render_to(self.screen, (400, 200), f"ROUND {self.round}",
                                         fgcolor=RED, bgcolor=GREEN)
            self.counting_font.render_to(self.screen, (500, 300), f"{self.counting}",
                                         fgcolor=RED, bgcolor=GREEN)

        pg.display.update()


"""
game type selection:

player0_role_id = 0, player1_role_id = 0, player0_role_id + player1_role_id = 0, both players are shooters, GameSS 
player0_role_id or player1_role_id = 1, player0_role_id + player1_role_id = 1, one shooter one chopper, GameSC 
player0_role_id = 1, player1_role_id = 1, player0_role_id + player1_role_id = 2, both players are choppers, GameCC 
"""
game_type_lst = [GameSS, GameSC, GameCC]