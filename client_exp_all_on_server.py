import pygame as pg
from sys import exit
import json
from collections import namedtuple
from platform_shooter_settings import *
from platform_shooter_sprites import *
import sprite_player_correction
from role_def import *
from network1 import Network


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.HWSURFACE)
        pg.display.set_caption(TITLE)
        # self.bg = pg.image.load("resources/platform/Tree_1024_768.png")
        # self.screen.blit(self.bg, (0, 0))
        self.clock = pg.time.Clock()

        # map list
        self.map_list = [0, 1]
        self.current_level_no = 0

        # match types
        self.match_types = ["Deathmatch", "1st23", "Best of 3"]

        # match score
        self.match_score = {"match_type": self.match_types[0], "round": 0, "shooter": 0, "chopper": 0,
                            "map": 0, "game_finished": False}

        # the "R" sign on the shooter's head to indicate it's the reloading time, so it can't shoot
        self.r_sign = DrawText(self.screen, 10, RED, 0, 0, "r_sign", "R", 0, 10)

        # flag to display or hide mouse location
        self.mouse_pos_flag = False

        # display the coordinates of the mouse position
        self.mouse_pos = DrawText(self.screen, 10, LIGHT_BLUE, 0, 730, "mouse_pos", "(0,0)")

        self.fps_txt = DrawText(self.screen, 5, LIGHT_GREEN, 5, 5, "fps_txt", "0")

        self.network = None
        self.player_id = 0
        self.svr_reply = None

        self.winner = None
        self.running = True
        self.playing = True

    def new(self):
        if self.match_score["game_finished"]:
            return
        else:
            self.match_score["round"] += 1

        # player score text display
        self.player_shooter_score = DrawText(self.screen, 20, WHITE, 100, 10, "shooter_score", "0")
        self.player_chopper_score = DrawText(self.screen, 20, WHITE, 600, 10, "chopper_score", "0")

        # Music and sound effect
        self.snd_yeet = pg.mixer.Sound("resources/sound/yeet.ogg")
        self.snd_yeet.set_volume(0.2)

        pg.mixer.music.load("resources/sound/Resurrection of the Dagger.ogg")
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(loops=-1)

        self.restart()

    def restart(self):
        # a string to represent key events
        # K_LEFT, K_RIGHT, K_UP, K_SPACE, K_a, K_d, K_w, K_c, up_LEFT, up_RIGHT, up_a, up_d
        self.keys = "1000000000000"  # the first letter can't be "0" otherwise it disconnect the server

        # match type
        match_type = self.match_score["match_type"]
        match_score = str(self.match_score["shooter"]) + " - " + match_type + " - " + str(self.match_score["chopper"])
        self.match_type_txt = DrawText(self.screen, 20, WHITE, 25, 720, "match_score", match_score, centered=True)

        # start a new game
        self.bullets = []

        bullet1 = Bullet(-100, 0, 'l', SCREEN_WIDTH)
        bullet2 = Bullet(-100, 0, 'l', SCREEN_WIDTH)
        bullet3 = Bullet(-100, 0, 'l', SCREEN_WIDTH)
        bullet4 = Bullet(-100, 0, 'l', SCREEN_WIDTH)
        bullet5 = Bullet(-100, 0, 'l', SCREEN_WIDTH)

        # Create the self.player
        self.player_shooter = Player()
        self.player_shooter.hit_limit = 3
        # self.player_shooter.score_text = DrawText(self.screen, 20, WHITE, 200, 10)

        self.player_chopper = sprite_player_correction.Player()
        self.player_chopper.hit_limit = 3

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

        self.active_sprite_list.add(self.player_shooter, self.player_chopper, self.fps_txt, self.match_type_txt,
                                    self.player_shooter_score, self.player_chopper_score)

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)  # not needed when all updates are calculated on server?
            self.events()
            # self.update()

            # player_id, role, pos_x, pos_y, img_dict_key, img_idx
            # game_state = self.svr_reply.decode
            # self.state0 = {"role0": self.roles[0], "pos0_x": 0, "pos0_y": 0, "img_dict_key0": "", "img_idx0": 0}
            # self.state1 = {"role1": self.roles[1], "pos1_x": 0, "pos1_y": 0, "img_dict_key1": "", "img_idx1": 0}
            self.player_shooter.rect.x = self.svr_reply[1]
            self.player_shooter.rect.y = self.svr_reply[2]
            # self.player_shooter.img_dict_key = self.svr_reply[5]
            # self.player_shooter.image_idx = self.svr_reply[6]
            self.player_shooter.update_img(self.svr_reply[3], self.svr_reply[4])

            self.player_chopper.rect.x = self.svr_reply[6]
            self.player_chopper.rect.y = self.svr_reply[7]
            self.player_chopper.update_img(self.svr_reply[8], self.svr_reply[9])
            self.draw()

        # music is unloaded in update() when the match is over
        # pg.mixer.music.unload()

    def events(self):
        # Game Loop - events
        # K_LEFT, K_RIGHT, K_UP, K_SPACE, K_a, K_d, K_w, K_c, up_LEFT, up_RIGHT, up_a, up_d
        self.keys = "000000000000"
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
                    self.chg_key(0, "1")
                if event.key == pg.K_RIGHT:
                    self.chg_key(1, "1")
                if event.key == pg.K_UP:
                    self.chg_key(2, "1")
                if event.key == pg.K_SPACE:
                    self.chg_key(3, "1")

                # player_chopper controls
                if event.key == pg.K_a:
                    self.chg_key(4, "1")
                elif event.key == pg.K_d:
                    self.chg_key(5, "1")
                if event.key == pg.K_w:
                    self.chg_key(6, "1")
                if event.key == pg.K_c:
                    self.chg_key(7, "1")

            if event.type == pg.KEYUP:
                # player_shooter controls
                if event.key == pg.K_LEFT:
                    self.chg_key(8, "1")
                if event.key == pg.K_RIGHT:
                    self.chg_key(9, "1")

                # player_chopper controls
                if event.key == pg.K_a:
                    self.chg_key(10, "1")
                if event.key == pg.K_d:
                    self.chg_key(11, "1")

        self.svr_reply = self.network.send(self.keys)
        # self.svr_reply = self.network.send("self.keys")

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

        self.network.game_state.update(0, "shooter", self.player_shooter.rect.x, self.player_shooter.rect.y,
                                       self.player_shooter.img_dict_key, self.player_shooter.image_idx)
        self.network.send(self.network.game_state)

        # need to receive chopper info here

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

    def draw(self):
        # Game Loop - draw
        self.current_level.draw(self.screen)
        self.active_sprite_list.draw(self.screen)
        self.bullet_sprite_grp.draw(self.screen)

        # *after* drawing everything, flip the display
        pg.display.update()

    def chg_key(self, position, new_letter):
        lst = list(self.keys)
        lst[position] = new_letter
        self.keys = "".join(lst)

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

    def show_start_screen(self):
        # game splash/start screen
        ip_valid_ltr = "0123456789."
        port_valid_ltr = "0123456789"
        background = pg.image.load("resources/gui/Window_06.png").convert_alpha()
        title = DrawText(self.screen, 50, GREEN, 350, 25, "title", "My Game", 0, 10)
        name = DrawText(self.screen, 35, WHITE, 150, 230, "name", "Your Name: ", 1, 27)
        server_IP = DrawText(self.screen, 35, WHITE, 150, 300, "server_ip", "Server IP: ", 1, 26, ip_valid_ltr)
        server_Port = DrawText(self.screen, 35, WHITE, 150, 370, "server_port", "Server Port#: ", 1, 19, port_valid_ltr)
        text_sprites = pg.sprite.Group()
        text_sprites.add(title, name, server_IP, server_Port)

        name.input_text = "tom"
        server_IP.input_text = '192.168.3.15'
        server_Port.input_text = "5050"

        settings_btn = Buttons("resources/gui/settings.png", 100, 500, "setting")
        start_btn = Buttons("resources/gui/right.png", 400, 500, "start")
        credit_btn = Buttons("resources/gui/credit.png", 700, 500, "credit")
        btn_sprites = pg.sprite.Group()
        btn_sprites.add(settings_btn, start_btn, credit_btn)

        pg.mixer.music.load("resources/sound/Designer_Stubble.ogg")
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(loops=-1)

        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # waiting = False
                    # self.running = False
                    pg.quit()
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    for txt in iter(text_sprites):
                        if txt.rect.collidepoint(pg.mouse.get_pos()):
                            txt.cursor = 1
                        else:
                            txt.cursor = 0
                    for btn in iter(btn_sprites):
                        if btn.rect.collidepoint(pg.mouse.get_pos()):
                            if btn.name == "start":
                                # update text to reflect changes before checking ip validity
                                text_sprites.update()
                                if server_IP.check_ip() == "stop":
                                    self.wait_for_key()
                                    break
                                elif server_Port.check_port() == "stop":
                                    self.wait_for_key()
                                    break
                                elif name.check_name() == "stop":
                                    self.wait_for_key()
                                    break
                                else:
                                    pg.mixer.music.fadeout(500)
                                    pg.mixer.music.unload()
                                    waiting = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_F1:
                        self.mouse_pos_flag = not self.mouse_pos_flag
                        if self.mouse_pos_flag:
                            text_sprites.add(self.mouse_pos)
                        else:
                            text_sprites.remove(self.mouse_pos)

                    if 32 <= event.key <= 126:
                        for txt in iter(text_sprites):
                            txt.add_letter(event.unicode)
                    elif event.key == pg.K_RETURN:
                        for txt in iter(text_sprites):
                            txt.finish()
                    elif event.key == pg.K_BACKSPACE:
                        for txt in iter(text_sprites):
                            txt.back_space()

            self.screen.blit(background, (0, 0))

            if self.mouse_pos in text_sprites:
                self.mouse_pos.text = f"({str(pg.mouse.get_pos()[0])},{str(pg.mouse.get_pos()[1])})"

            text_sprites.update()
            text_sprites.draw(self.screen)
            btn_sprites.draw(self.screen)

            pg.display.flip()

        self.network = Network(server_IP.input_text, server_Port.input_text)
        self.player_id = self.network.game_state.player_id

    def show_select_screen(self):
        background = pg.image.load("resources/gui/Window_06.png").convert_alpha()

        self.match_score = {"match_type": self.match_types[0], "round": 0, "shooter": 0, "chopper": 0,
                            "map": 0, "game_finished": False}

        match_type_txt_lst = []
        for match in self.match_types:
            txt = DrawText(self.screen, 35, GREEN, 0, 35, match, match, 0, 10, centered=True)
            match_type_txt_lst.append(txt)
        match_select = pg.sprite.GroupSingle(match_type_txt_lst[0])

        map_txt_lst = []
        for i in range(len(self.map_list)):
            txt = DrawText(self.screen, 35, GREEN, 0, 700, "map"+str(i), "map"+str(i), 0, 10, centered=True)
            map_txt_lst.append(txt)
        map_select = pg.sprite.GroupSingle(map_txt_lst[0])

        girl_page = pg.sprite.Group()
        for item in girl_txt:
            description = DrawText(self.screen, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7])
            girl_page.add(description)
        role_girl = PlayerIdle(idle_girl, (320, 150))
        girl_page.add(role_girl)

        boy_page = pg.sprite.Group()
        for item in boy_txt:
            description = DrawText(self.screen, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7])
            boy_page.add(description)
        role_boy = PlayerIdle(idle_boy, (360, 210))
        boy_page.add(role_boy)

        role_lst = [girl_page, boy_page]

        right_btn_match = Buttons("resources/gui/right_small.png", 760, 60, "right_match")
        left_btn_match = Buttons("resources/gui/left_small.png", 160, 60, "left_match")

        right_btn_map = Buttons("resources/gui/right_small.png", 760, 660, "right_map")
        left_btn_map = Buttons("resources/gui/left_small.png", 160, 660, "left_map")

        left_btn = Buttons("resources/gui/left.png", 100, 200, "left")
        right_btn = Buttons("resources/gui/right.png", 700, 200, "right")
        go_btn = Buttons("resources/gui/Button_18_small.png", 870, 600, "go")
        btn_sprites = pg.sprite.Group()
        btn_sprites.add(left_btn, right_btn, go_btn, right_btn_match, left_btn_match, left_btn_map, right_btn_map)

        pg.mixer.music.load("resources/sound/Amazon.ogg")
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(loops=-1)

        waiting = True
        page_idx = 0
        match_idx = 0
        map_idx = 0
        mouse_pos_grp = pg.sprite.GroupSingle()
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_F1:
                        self.mouse_pos_flag = not self.mouse_pos_flag
                        if self.mouse_pos_flag:
                            mouse_pos_grp.add(self.mouse_pos)
                        else:
                            mouse_pos_grp.remove(self.mouse_pos)

                if event.type == pg.MOUSEBUTTONDOWN:
                    for btn in iter(btn_sprites):
                        if btn.rect.collidepoint(pg.mouse.get_pos()):
                            if btn.name == "go":
                                pg.mixer.music.fadeout(500)
                                pg.mixer.music.unload()
                                waiting = False
                            elif btn.name == "left":
                                if page_idx - 1 < 0:
                                    page_idx = len(role_lst) - 1
                                else:
                                    page_idx -= 1
                            elif btn.name == "right":
                                if page_idx + 1 == len(role_lst):
                                    page_idx = 0
                                else:
                                    page_idx += 1
                            elif btn.name == "left_match":
                                if match_idx - 1 < 0:
                                    match_idx = len(match_type_txt_lst) - 1
                                else:
                                    match_idx -= 1
                                match_select.empty()
                                match_select.add(match_type_txt_lst[match_idx])
                                self.match_score["match_type"] = self.match_types[match_idx]
                            elif btn.name == "right_match":
                                if match_idx + 1 == len(match_type_txt_lst):
                                    match_idx = 0
                                else:
                                    match_idx += 1
                                match_select.empty()
                                match_select.add(match_type_txt_lst[match_idx])
                                self.match_score["match_type"] = self.match_types[match_idx]
                            elif btn.name == "left_map":
                                if map_idx - 1 < 0:
                                    map_idx = len(map_txt_lst) - 1
                                else:
                                    map_idx -= 1
                                map_select.empty()
                                map_select.add(map_txt_lst[map_idx])
                                self.current_level_no = map_idx
                            elif btn.name == "right_map":
                                if map_idx + 1 == len(map_txt_lst):
                                    map_idx = 0
                                else:
                                    map_idx += 1
                                map_select.empty()
                                map_select.add(map_txt_lst[map_idx])
                                self.current_level_no = map_idx

            self.screen.blit(background, (0, 0))

            if self.mouse_pos in mouse_pos_grp:
                self.mouse_pos.text = f"({str(pg.mouse.get_pos()[0])},{str(pg.mouse.get_pos()[1])})"

            # update role information on the page
            role_lst[page_idx].update()
            match_select.update()
            map_select.update()
            mouse_pos_grp.update()

            role_lst[page_idx].draw(self.screen)
            btn_sprites.draw(self.screen)
            match_select.draw(self.screen)
            map_select.draw(self.screen)
            mouse_pos_grp.draw(self.screen)

            self.network.send(self)

            pg.display.flip()

    def show_go_screen(self):

        # unload the music playing during game, can change to the music on the go_screen
        pg.mixer.music.fadeout(500)
        pg.mixer.music.unload()
        # game over/reset/continue
        if not self.running:
            return
        # pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        # pg.mixer.music.play(loops=-1)
        self.screen.fill(BLACK)
        game_over_text = DrawText(self.screen, 60, WHITE, 0, SCREEN_HEIGHT / 4, "game_over", "GAME OVER",
                                  centered=True)
        match_type = self.match_score["match_type"]
        winner_text = DrawText(self.screen, 50, WHITE, 0, SCREEN_HEIGHT/2, "winner",
                               f"{match_type}: {self.winner} WINS!", centered=True)
        # self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        press_key_text = DrawText(self.screen, 40, WHITE, 0, SCREEN_HEIGHT * 3 / 4, "press_key",
                                  "Press a key to play again", centered=True)
        # if self.score > self.highscore:
        #     self.highscore = self.score
        #     self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        #     with open(path.join(self.dir, HS_FILE), 'w') as f:
        #         f.write(str(self.score))
        # else:
        #     self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)

        txt_sprites = pg.sprite.Group()
        txt_sprites.add(game_over_text, winner_text, press_key_text)

        txt_sprites.update()
        txt_sprites.draw(self.screen)

        pg.display.flip()

        pg.time.wait(1000)
        self.wait_for_key()

        # pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        # clear the event queue in case there are anything buffered there
        pg.event.clear()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False


g = Game()
g.show_start_screen()
while g.running:
    # g.show_select_screen()
    g.new()
    # g.show_go_screen()

pg.quit()