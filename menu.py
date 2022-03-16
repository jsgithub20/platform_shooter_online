"""
File_id: 07oct2021_menu
Related file id:  07oct2021_async_client, 07oct2021_async_server
This is the alpha player menu code for the "shooter" game
"""
import time
from threading import Thread
from pygame_menu.locals import *
from typing import Optional
from logging import handlers
import logging
import coloredlogs
import queue
import pygame
import pygame_menu
import asyncio
import async_client
import pygame.freetype as ft
import role_def
import game_class_c
from platform_shooter_settings import *

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
FPS = 60
WINDOW_SIZE = (1024, 768)
GAME_ROOMS = ["Amy's game", "Jacky's game", "Dora's game", "Amy's game", "Jacky's game", "Dora's game",
              "Amy's game", "Jacky's game", "Dora's game", "Amy's game", "Jacky's game", "Dora's game"]
TIMEOUT = 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (68, 105, 252)
LIGHT_GREEN = (100, 250, 122)

# -----------------------------------------------------------------------------
# Load image & set game text
# -----------------------------------------------------------------------------
background_image = pygame.image.load("resources\gui\Window_19_1024-768.png")

GIRL_idle_img = []
for i in range(9):
    GIRL_idle_img.append(pygame_menu.BaseImage(f"resources/gui/girl/Idle__00{i}.png"))
BOY_idle_img = []
for i in range(9):
    BOY_idle_img.append(pygame_menu.BaseImage(f"resources/gui/boy/Idle__00{i}.png"))


# -----------------------------------------------------------------------------
# Methods


class DrawText(pygame.sprite.Sprite):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.font = pygame.font.Font("resources/OvOV20.ttf", 30)
        self.image = self.font.render(text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.change_x = 0
        self.change_y = 0
        self.speed = 6

    def update(self) -> None:
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        self.image = self.font.render(self.text, True, (255, 255, 255))

    def go_left(self):
        self.change_x = -self.speed

    def go_right(self):
        self.change_x = self.speed

    def go_up(self):
        self.change_y = -self.speed

    def go_down(self):
        self.change_y = self.speed

    def stop(self):
        self.change_x = 0
        self.change_y = 0

    def pos(self):
        return self.rect.x, self.rect.y


class EventLoop(Thread):
    def __init__(self):
        self._loop = asyncio.new_event_loop()
        super().__init__(target=self._loop.run_forever, daemon=True)
        self.start()
        self.game_task = None

    def stop(self):
        self._loop.call_soon_threadsafe(self._loop.stop)

    def stop_tasks(self):
        for task in asyncio.tasks.all_tasks(self._loop):
            self._loop.call_soon_threadsafe(task.cancel)
            done = False
            while not done:
                done = task.done()

    def create_task(self, coro):
        self.game_task = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return self.game_task


class MyLogger:
    def __init__(self):
        FIELD_STYLES = {'asctime': {'color': 'green'},
                        'levelname': {'bold': False, 'color': (200, 200, 200)},
                        'filename': {'color': 'cyan'},
                        'funcName': {'color': 'blue'}}

        LEVEL_STYLES = {'critical': {'bold': True, 'color': 'red'},
                        'debug': {'color': 'magenta'},
                        'error': {'color': 'red'},
                        'exception': {'color': 'red'},
                        'info': {'color': 'green'},
                        'warning': {'color': 'yellow'}}

        self.my_logger = logging.getLogger()

        format = '%(asctime)s [%(levelname)s] - %(message)s'

        coloredlogs.install(level=logging.INFO,
                            logger=self.my_logger,
                            fmt=format,
                            field_styles=FIELD_STYLES,
                            level_styles=LEVEL_STYLES)

        format_str = logging.Formatter(format)
        fh = handlers.RotatingFileHandler("client_log.txt", "a", 100000, 3)
        fh.setFormatter(format_str)
        self.my_logger.addHandler(fh)


class Menu:
    def __init__(self):
        pygame.init()
        self.playing = True
        self.my_logger = MyLogger()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)  # , flags=pygame.NOFRAME)
        self.room_selected1 = "Join an existing game: "
        self.room_selected2 = "<click to choose>"
        self.t_loop = EventLoop()
        self.connection: Optional[async_client.Network] = None
        self.connected_flag = False
        self.server_ip = "47.94.100.39"
        self.server_port = "8887"
        self.my_name = ""
        self.game_rooms = [("No game", False, 1), ]  # [[player0_name, game_ready, room_id],]
        self.chosen_room: None  # [player0_name, game_ready, room_id], same as dropselect item
        self.room_frame = None
        self.conn_type = "handshake"  # "create" or "join"
        self.client_id = "0"
        self.opponent_name = ""
        self.map_id = 0
        self.match_id = 0
        self.level_id = 0
        self.role_id = 0
        self.player_id = 0
        self.gs_lst = []  # Game state received as a list
        self.splat_font = ft.Font("resources/fonts/earwig factory rg.ttf", 60)
        self.main_menu: [pygame_menu.menu] = None
        self.b_connect: [pygame_menu.widgets.widget.button] = None
        self.selector_game: [pygame_menu.widgets.widget.selector] = None
        self.surface: [pygame.Surface] = pygame.image.load("resources/gui/Window_06.png")
        self.sound: [pygame_menu.sound.Sound] = None

        girl_idle = []

        for j in range(9):
            girl_idle.append(pygame.image.load(f"resources/gui/girl/Idle__00{j}.png"))

        boy_idle = []

        for j in range(9):
            boy_idle.append(pygame.image.load(f"resources/gui/boy/Idle__00{j}.png"))

        self.img_lst = [girl_idle, boy_idle]

        self.current_role_id = 0
        self.previous_role_id = 1
        self.current_img_lst = self.img_lst[self.current_role_id]

        self.girl_desc_lbl_lst = []
        self.boy_desc_lbl_lst = []

        self.lbl_lst = [self.girl_desc_lbl_lst, self.boy_desc_lbl_lst]

    def cb_conn_conn(self, server_ip, server_port, player_name, **kwargs):
        if not self.connected_flag:
            self.connected_flag = True
        else:
            kwargs["widget"].set_title(f"Connection status: already connected with client id - {self.client_id}")
            return
        self.server_ip = server_ip.get_value()
        self.server_port = server_port.get_value()
        self.my_name = player_name.get_value()
        pygame.display.set_caption(f"{self.my_name}'s Game Window")
        self.connection = async_client.Network(self.server_ip, self.server_port)
        conn_result = self.t_loop.create_task(self.connection.conn(self.my_name))
        try:
            # this connection should be established immediately otherwise there's a network issue
            conn_result.result(TIMEOUT)
            self.client_id = self.connection.client_id
        except Exception as e:
            kwargs["widget"].set_title(f"Connection status: error - {e}")
            self.my_logger.my_logger.error(f"Connection status: error - {e}")
        else:
            kwargs["widget"].set_title(f"Connection status: connected with client id - {self.client_id}")
            self.my_logger.my_logger.info(f"Connected to server: {self.server_ip}:{self.server_port} "
                                          f"with client id - {self.client_id}")

    def cb_conn_create(self):
        self.conn_type = "create"
        self.t_loop.create_task(self.connection.create())
        self.t_loop.create_task(self.connection.client())
        self.demo_game()

    def cb_selection_menu_opened(self, from_menu, to_menu):
        self.conn_type = "create"
        self.t_loop.create_task(self.connection.create())
        self.t_loop.create_task(self.connection.client_game())

    def cb_play(self):
        self.demo_game()

    def conn_join(self):
        task = self.t_loop.create_task(self.connection.join())
        try:
            # this connection should be established immediately otherwise there's a network issue
            task.result(TIMEOUT)
            self.game_rooms = self.connection.game_rooms
            self.game_rooms = [tuple(lst) for lst in self.game_rooms]
            self.selector_game.update_items(self.game_rooms)
            self.chosen_room = self.selector_game.get_items()[0]  # Default choice is the first game room
        except Exception as e:
            self.my_logger.my_logger.error(f"Connection issue during joining - {e}")

    def cb_role_sel_lft(self):
        if self.current_role_id - 1 < 0:
            self.current_role_id = len(self.img_lst) - 1
        else:
            self.current_role_id -= 1

        current_lbl_lst = self.lbl_lst[self.current_role_id]
        previous_lbl_lst = self.lbl_lst[self.previous_role_id]

        for j in range(len(current_lbl_lst)):
            current_lbl_lst[j].show()
            previous_lbl_lst[j].hide()

        self.previous_role_id = self.current_role_id

        self.current_img_lst = self.img_lst[self.current_role_id]

    # def cb_join_game_btn(self):
    #     self.t_loop.create_task(self.connection.send_room_choice(self.chosen_room))
    #     self.t_loop.create_task(self.connection.client_game())
        # self.demo_game()

    def cb_dropselector_game_onchange(self, item_index: tuple, game_ready, room_id):
        # [(player0_name, game_ready, room_id),]
        self.chosen_room = item_index[0]

    def cb_join_menu_openned(self, from_menu, to_menu):
        self.conn_join()

    def cb_refresh(self):
        # self.game_rooms
        task = self.t_loop.create_task(self.connection.refresh())
        try:
            # this connection should be established immediately otherwise there's a network issue
            task.result(TIMEOUT)
            self.game_rooms = self.connection.game_rooms
            self.game_rooms = [tuple(lst) for lst in self.game_rooms]
            self.selector_game.update_items(self.game_rooms)
            # self.selector_game.render()
        except asyncio.TimeoutError:
            self.my_logger.my_logger.error(f"Connection issue to server during refreshing")

    def cb_selector_map_onchange(self, item_tuple, *args, **kwargs):
        self.map_id = item_tuple[1]

    def cb_selector_match_type_onchange(self, item_tuple, *args, **kwargs):
        self.match_id = item_tuple[1]

    def cb_player0_wait_menu_opened(self, from_menu, to_menu):
        self.player_id = 0
        self.connection.game_setting = [1, self.map_id, self.match_id, self.current_role_id]
        # self.t_loop.create_task(self.connection.client_game())

        self.game()

    def cb_player1_wait_menu_opened(self, from_menu, to_menu):
        self.player_id = 1
        self.t_loop.create_task(self.connection.send_room_choice(self.chosen_room))
        self.t_loop.create_task(self.connection.client_game())

        self.game()

    def game(self):
        self.main_menu.disable()

        while not self.connection.game_ready:
            self.clock.tick(FPS)
            self.screen.fill((0, 200, 0))
            if self.player_id == 0:
                self.splat_font.render_to(self.screen, (100, 200), "Waiting for 2nd player")
            else:
                self.splat_font.render_to(self.screen, (100, 200), "Waiting for 1st player to set the game")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.t_loop.stop_tasks()
                    self.t_loop.stop()
                    pygame.quit()
                    exit()
            pygame.display.flip()

        self.opponent_name = self.connection.server_msg[1]
        self.map_id = self.connection.server_msg[2]
        self.match_id = self.connection.server_msg[3]
        self.role_id = self.connection.server_msg[4]
        g = game_class_c.Game(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, self.map_id, self.match_id, self.role_id)
        g.new()

        while g.playing:  # routine game tick
            g.events()
            self.connection.events_str = g.events_str
            try:
                self.gs_lst = self.connection.game_state.get(timeout=1)
                # self.gs_lst = self.connection.game_state.get()
            except queue.Empty:
                # TODO: code to acknowledge the player and ask for input
                print("Connection issue")
                g.playing = False
                pass

            g.update_game_state(self.gs_lst)
            g.draw()

        pygame.quit()
        exit()

    def demo_game(self):
        self.main_menu.disable()

        player_disconnected_flag = False  # if the other player is disconnected, this will be set to True
        my_msg = DrawText("My msg:")
        their_msg = DrawText(f"{self.connection.server_msg}")
        msg_grp = pygame.sprite.Group()
        msg_grp.add(my_msg, their_msg)
        while True:
            self.clock.tick(60)
            self.screen.fill((0, 200, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.t_loop.stop_tasks()
                    self.t_loop.stop()
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.t_loop.stop_tasks()
                        self.t_loop.stop()
                        pygame.quit()
                        exit()
                    if event.key == pygame.K_SPACE:
                        self.connection.pos_send[0] += 1
                        self.connection.pos_send[1] += 1
                    if event.key == pygame.K_LEFT:
                        my_msg.go_left()
                    if event.key == pygame.K_RIGHT:
                        my_msg.go_right()
                    if event.key == pygame.K_UP:
                        my_msg.go_up()
                    if event.key == pygame.K_DOWN:
                        my_msg.go_down()
                if event.type == pygame.KEYUP:
                    my_msg.stop()

            if self.connection.server_msg[0] != "Game Ready":
                my_msg.rect.x, my_msg.rect.y = (100, 100)
                their_msg.rect.x, their_msg.rect.y = (100, 200)
            elif not player_disconnected_flag:
                try:
                    # 3 lines of get_nowait() to make sure even the Queue() is full, only the last item is returned
                    their_msg.rect.x, their_msg.rect.y = self.connection.pos_recv.get_nowait()
                    their_msg.rect.x, their_msg.rect.y = self.connection.pos_recv.get_nowait()
                    their_msg.rect.x, their_msg.rect.y = self.connection.pos_recv.get_nowait()
                except queue.Empty:
                    pass
            else:
                their_msg.rect.x, their_msg.rect.y = (200, 200)

            my_msg.text = f"{self.my_name}'s client {self.connection.client_id}, {str((my_msg.rect.x, my_msg.rect.y))}"
            if their_msg.rect.x == their_msg.rect.y == -99:
                player_disconnected_flag = True

            if player_disconnected_flag:
                their_msg.text = f"Player '{self.connection.opponent_name}' is disconnected from the server"
            else:
                their_msg.text = f"{self.connection.server_msg[1]}, {str((their_msg.rect.x, their_msg.rect.y))}"

            self.connection.pos_send = my_msg.pos()

            msg_grp.update()
            msg_grp.draw(self.screen)

            pygame.display.flip()

    def main(self, test: bool = False) -> None:
        """
        Main program.
        :param test: Indicate function is being tested
        :return: None
        """

        all_sound = pygame_menu.sound.Sound()
        # engine.set_sound(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, 'resources/sound/Designer_Stubble.ogg', volume=0.5)
        all_sound.set_sound(pygame_menu.sound.SOUND_TYPE_OPEN_MENU, 'resources/sound/Amazon.ogg', volume=0.5)
        # all_sound.play_open_menu()
        # engine.play_click_mouse()

        # -------------------------------------------------------------------------
        # Create menus: Main menu
        # -------------------------------------------------------------------------
        no_title_theme = pygame_menu.themes.THEME_ORANGE.copy()
        # no_title_theme.title_background_color = (0, 0, 0, 0)
        no_title_theme.title_font = pygame_menu.font.FONT_8BIT

        no_title_theme.title_font_shadow = True
        no_title_theme.title_font_color = (200, 50, 50)
        no_title_theme.title_close_button = False
        no_title_theme.title_offset = (120, 0)

        no_title_theme.background_color = (0, 0, 0, 10)
        # no_title_theme.title = False
        no_title_theme.widget_font = pygame_menu.font.FONT_MUNRO
        no_title_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        no_title_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        no_title_theme.widget_padding = 15

        no_title_theme_join_game = pygame_menu.themes.THEME_ORANGE.copy()
        no_title_theme_join_game.background_color = (0, 0, 0, 10)
        # no_title_theme_join_game.title = False
        no_title_theme_join_game.title_close_button = False
        no_title_theme_join_game.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        no_title_theme_join_game.title_offset = (200, 0)
        no_title_theme_join_game.title_font_shadow = True
        no_title_theme_join_game.title_font_color = (200, 50, 50)
        no_title_theme_join_game.widget_font = pygame_menu.font.FONT_MUNRO

        no_title_theme_join_game.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        # no_title_theme_join_game.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
        no_title_theme_join_game.widget_padding = 5

        sub_menu_selection_theme = pygame_menu.themes.THEME_ORANGE.copy()
        sub_menu_selection_theme.background_color = (0, 0, 0, 0)
        sub_menu_selection_theme.title_close_button = False
        sub_menu_selection_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        sub_menu_selection_theme.title_offset = (200, 0)
        sub_menu_selection_theme.title_font_shadow = True
        sub_menu_selection_theme.title_font_color = (200, 50, 50)
        sub_menu_selection_theme.widget_font = "resources/OvOV20.ttf"
        sub_menu_selection_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        sub_menu_selection_theme.widget_padding = 5

        self.main_menu = pygame_menu.Menu(
            "Platform Game", WINDOW_SIZE[0] * 0.8, WINDOW_SIZE[1] * 0.8,
            center_content=False,
            # onclose=pygame_menu.events.EXIT,  # User press ESC button
            theme=no_title_theme,
            position=[40, 30],
        )

        self.join_game_menu = pygame_menu.Menu(
            'Choosing Games', WINDOW_SIZE[0] * 0.8, WINDOW_SIZE[1] * 0.8,
            center_content=False,
            # onclose=pygame_menu.events.EXIT,  # User press ESC button
            theme=no_title_theme_join_game,
            position=[40, 20],
        )

        self.join_game_menu.set_onbeforeopen(self.cb_join_menu_openned)

        self.sub_menu_selection = pygame_menu.Menu(
            'Choosing Games', 1024, 768,
            center_content=False,
            onclose=pygame_menu.events.EXIT,  # User press ESC button
            theme=sub_menu_selection_theme,
            position=[40, 20])

        self.sub_menu_selection.set_onbeforeopen(self.cb_selection_menu_opened)

        self.sub_menu_player0_wait = pygame_menu.Menu(
            'Waiting for player', 1024, 768,
            center_content=False,
            onclose=pygame_menu.events.EXIT,  # User press ESC button
            theme=sub_menu_selection_theme,
            position=[40, 20])

        self.sub_menu_player0_wait.set_onbeforeopen(self.cb_player0_wait_menu_opened)

        wait_lbl = self.sub_menu_player0_wait.add.label("Wait for the 2nd player to join...")
        wait_lbl.set_float(True, False, True)
        wait_lbl.translate(100, 300)

        self.sub_menu_player1_wait = pygame_menu.Menu(
            'Waiting for player', 1024, 768,
            center_content=False,
            onclose=pygame_menu.events.EXIT,  # User press ESC button
            theme=sub_menu_selection_theme,
            position=[40, 20])

        self.sub_menu_player1_wait.set_onbeforeopen(self.cb_player1_wait_menu_opened)

        wait_lbl = self.sub_menu_player1_wait.add.label("Wait for the 1st player to set the game...")
        wait_lbl.set_float(True, False, True)
        wait_lbl.translate(100, 300)

        self.main_menu.add.vertical_margin(30)

        server_ip = self.main_menu.add.text_input(
            'Server ip address: ',
            default='127.0.0.1',  # '47.94.100.39'
            onreturn=None,
            textinput_id='server_ip')

        server_port = self.main_menu.add.text_input(
            'Server port#: ',
            default='8887',
            onreturn=None,
            textinput_id='server_port')

        player_name = self.main_menu.add.text_input(
            'Your name: ',
            default="Amy",
            onreturn=None,
            textinput_id='new_game'
        )

        b_connect = self.main_menu.add.button("Connection status: <click to connect>",
                                              self.cb_conn_conn,
                                              server_ip,
                                              server_port,
                                              player_name)
        b_connect.add_self_to_kwargs()

        b_create = self.main_menu.add.button("Create a new game", self.sub_menu_selection)
        # b_create.add_self_to_kwargs()

        self.main_menu.add.button("Choose an existing game to join", self.join_game_menu)

        self.join_game_menu.add.vertical_margin(30)

        refresh_frame = self.join_game_menu.add.frame_h(400, 50, align=ALIGN_LEFT)

        b_refresh = self.join_game_menu.add.button("refresh",
                                                   self.cb_refresh,
                                                   underline=True,
                                                   cursor=CURSOR_HAND)

        # b_refresh.add_self_to_kwargs()

        refresh_frame.pack(self.join_game_menu.add.label("Please"))
        refresh_frame.pack(b_refresh)
        refresh_frame.pack(self.join_game_menu.add.label(" the game list!"))

        self.join_game_menu.add.vertical_margin(15)

        self.selector_game = self.join_game_menu.add.dropselect(
            title='Choose a game to join:',
            items=self.game_rooms,
            default=0,
            onchange=self.cb_dropselector_game_onchange,
            selection_box_bgcolor=(200, 200, 50),
            selection_box_height=10
        )

        self.join_game_menu.add.vertical_margin(15)

        self.join_game_menu.add.button("Join", self.sub_menu_player1_wait, cursor=CURSOR_HAND)
        self.join_game_menu.add.vertical_margin(15)
        #
        # self.join_game_menu.add.button("Back", pygame_menu.events.BACK)
        # self.join_game_menu.add.vertical_margin(15)

        self.join_game_menu.add.button("Quit", pygame_menu.events.EXIT)

        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)
        self.main_menu.add.vertical_margin(50)
        self.main_menu.add.label("Disclaimer: you agree to use this program on your own risks.",
                                 font_color="red",
                                 font_size=20,
                                 align=ALIGN_CENTER)
        self.main_menu.set_sound(all_sound, recursive=True)  # Apply on menu and all sub-menus

        lbl_match_type = self.sub_menu_selection.add.label("Match Types")
        lbl_match_type.set_float(True, False, True)
        lbl_match_type.translate(100, 60)

        selector_match_type = self.sub_menu_selection.add.dropselect(
            title='',
            items=[("Deathmatch", 0),
                   ("1st23", 1),
                   ("Best of 3", 2)],
            default=0,
            font_size=26,
            selection_box_width=200,
            selection_box_height=100,
            selection_option_padding=(0, 5),
            selection_option_font_size=20,
            onchange=self.cb_selector_match_type_onchange
        )
        selector_match_type.set_float(True, False, True)
        selector_match_type.translate(60, 100)

        lbl_map = self.sub_menu_selection.add.label("Map Selection")
        lbl_map.set_float(True, False, True)
        lbl_map.translate(680, 60)

        selector_map = self.sub_menu_selection.add.dropselect(
            title='',
            items=[("Map0", 0),
                   ("Map1", 1),
                   ("Map3", 2)],
            default=0,
            font_size=26,
            selection_box_width=200,
            selection_box_height=100,
            selection_option_padding=(0, 5),
            selection_option_font_size=20,
            onchange=self.cb_selector_map_onchange
        )
        selector_map.set_float(True, False, True)
        selector_map.translate(650, 100)

        btn_img_lft = pygame_menu.BaseImage("resources/gui/left.png")

        # title text can't be empty, otherwise resize doesn't work!
        sub1_btn_lft = self.sub_menu_selection.add.button(" ", self.cb_role_sel_lft, background_color=btn_img_lft)
        sub1_btn_lft.resize(100, 100)
        sub1_btn_lft.set_float(True, False, True)
        sub1_btn_lft.translate(150, 200)

        btn_img_rgt = pygame_menu.BaseImage("resources/gui/right.png")

        sub1_btn_rgt = self.sub_menu_selection.add.button(" ", None, background_color=btn_img_rgt)
        sub1_btn_rgt.resize(100, 100)
        sub1_btn_rgt.set_float(True, False, True)
        sub1_btn_rgt.translate(750, 200)

        for j in range(len(role_def.girl_txt)):
            lbl = self.sub_menu_selection.add.label(role_def.girl_txt[j][5],
                                                    "",
                                                    font_size=role_def.girl_txt[j][0],
                                                    font_color=role_def.girl_txt[j][1])
            lbl.set_float(True, False, True)
            lbl.translate(role_def.girl_txt[j][2], role_def.girl_txt[j][3])
            self.girl_desc_lbl_lst.append(lbl)

        for j in range(len(role_def.boy_txt)):
            lbl = self.sub_menu_selection.add.label(role_def.boy_txt[j][5],
                                                    "",
                                                    font_size=role_def.boy_txt[j][0],
                                                    font_color=role_def.boy_txt[j][1])
            lbl.set_float(True, False, True)
            lbl.translate(role_def.boy_txt[j][2], role_def.boy_txt[j][3])
            lbl.hide()
            self.boy_desc_lbl_lst.append(lbl)

        btn_img_ok = pygame_menu.BaseImage("resources/gui/Button_18_small.png")

        ok_btn = self.sub_menu_selection.add.button(" ", self.sub_menu_player0_wait, background_color=btn_img_ok)
        ok_btn.resize(100, 100)
        ok_btn.set_float(True, False, True)
        ok_btn.translate(890, 570)

        img = self.sub_menu_selection.add.surface(self.current_img_lst[0])
        img.set_float(True, False, True)
        img.translate(350, 100)

        img_idx = 0
        current_img_idx = 0
        # -------------------------------------------------------------------------
        # Main loop
        # -------------------------------------------------------------------------
        while self.playing:
            self.clock.tick(FPS)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.main_menu.update(events)
            # self.join_game_menu.update(events)

            if self.main_menu.is_enabled():
                self.screen.blit(background_image, (0, 0))
                if self.main_menu.is_enabled():
                    self.main_menu.draw(self.screen)
            else:
                break

            if img_idx + 1 == len(self.current_img_lst) * 2:
                img_idx = 0
            else:
                img_idx += 1

            if img_idx // 2 != current_img_idx:
                img.set_surface(self.current_img_lst[img_idx // 2])

            # Main menu
            # self.main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)

            # Flip surface
            pygame.display.flip()

            # At first loop returns
            if test:
                break


m = Menu()
if __name__ == '__main__':
    m.main()
    # game_window()
    # pygame.quit()
