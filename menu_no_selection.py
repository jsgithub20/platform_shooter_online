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

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
FPS = 60
WINDOW_SIZE = (1024, 768)
GAME_ROOMS = ["Amy's game", "Jacky's game", "Dora's game", "Amy's game", "Jacky's game", "Dora's game",
              "Amy's game", "Jacky's game", "Dora's game", "Amy's game", "Jacky's game", "Dora's game"]

# -----------------------------------------------------------------------------
# Load image
# -----------------------------------------------------------------------------
background_image = pygame.image.load("resources\gui\Window_19_1024-768.png")


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
        self._loop = asyncio.get_event_loop()
        super().__init__(target=self._loop.run_forever, daemon=True)
        self.start()
        self.game_task = None

    def stop(self):
        self._loop.call_soon_threadsafe(self._loop.stop)

    def create_task(self, coro):
        self.game_task = asyncio.run_coroutine_threadsafe(coro, self._loop)


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
        self.my_logger = MyLogger()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(WINDOW_SIZE, flags=pygame.NOFRAME)
        self.room_selected1 = "Join an existing game: "
        self.room_selected2 = "<click to choose>"
        self.t_loop = EventLoop()
        self.connection: Optional[async_client.Network] = None
        self.server_ip = "47.94.100.39"
        self.server_port = "8887"
        self.player_name = ""
        self.game_rooms = [("No game", False, 1), ]  # [[player0_name, game_ready, room_id],]
        self.chosen_room_id: str = "0"  # used to retrieve room info from game_dict on server
        self.room_frame = None
        self.start_type = "handshake"  # "create" or "join"
        self.client_id = "0"
        self.main_menu: [pygame_menu.menu] = None
        self.b_connect: [pygame_menu.widgets.widget.button] = None
        self.selector_game: [pygame_menu.widgets.widget.selector] = None
        self.surface: [pygame.Surface] = pygame.image.load("resources/gui/Window_06.png")
        self.sound: [pygame_menu.sound.Sound] = None

    def conn_conn(self, server_ip, server_port, player_name, **kwargs):
        self.server_ip = server_ip
        self.server_port = server_port
        self.player_name = player_name
        self.connection = async_client.Network(self.server_ip, self.server_port)
        self.t_loop.create_task(self.connection.conn(self.player_name))
        try:
            self.t_loop.game_task.result()
            self.client_id = self.connection.client_id
        except Exception as e:
            kwargs["widget"].set_title(f"Connection status: error - {e}")
            self.my_logger.my_logger.error(f"Connection status: error - {e}")
        else:
            kwargs["widget"].set_title(f"Connection status: connected with client id - {self.client_id}")
            self.my_logger.my_logger.info(f"Connected to server: {self.server_ip}:{self.server_port}")

    def conn_create(self):
        self.start_type = "create"
        self.t_loop.create_task(self.connection.create(self.player_name, self.start_type))
        try:
            self.t_loop.game_task.result()
        except Exception as e:
            kwargs["widget"].set_title(f"Connection status: error - {e}")
            self.my_logger.my_logger.error(f"Connection status: error - {e}")
        else:
            kwargs["widget"].set_title(f"Connection status: connected with client id - {self.client_id}")
            self.my_logger.my_logger.info(f"Connected to server: {self.server_ip}:{self.server_port}")

    def refresh(self):
        current_game_rooms = self.game_rooms
        try:
            print(f"starting 'try', q size = {self.connection.q_game_rooms.qsize()}")
            # 3 lines of get_nowait() to make sure even the Queue() is full, only the last item is returned
            self.game_rooms = self.connection.q_game_rooms.get_nowait()
            print(f"get from q: {self.game_rooms}")
            self.game_rooms = self.connection.q_game_rooms.get_nowait()
            self.game_rooms = self.connection.q_game_rooms.get_nowait()
        except queue.Empty:
            pass
        finally:
            # change [[..],] to [(..),] to fit requirement as items in dropselect
            # only update the game room list if the received list is different than current
            if self.game_rooms != current_game_rooms:
                self.game_rooms = [tuple(lst) for lst in self.game_rooms]
                self.selector_game.update_items(self.game_rooms)
                self.selector_game.render()  # force re-render the dropselect object

    def join(self, server_ip, server_port, player_name):
        self.start_type = "join"
        self.demo_game(server_ip, server_port, player_name)


    def demo_game(self, server_ip, server_port, player_name):
        self.server_ip = server_ip
        self.server_port = server_port
        self.player_name = player_name
        self.conn_task(server_ip, server_port, player_name)

        self.main_menu.disable()

        my_msg = DrawText("My msg:")
        their_msg = DrawText("Their msg:")
        msg_grp = pygame.sprite.Group()
        msg_grp.add(my_msg, their_msg)
        while True:
            self.clock.tick(60)
            self.screen.fill((0, 200, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.t_loop.game_task.cancel()
                    self.t_loop.stop()
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.t_loop.game_task.cancel()
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

            if self.connection.server_msg != "Game Ready":
                my_msg.rect.x, my_msg.rect.y = (100, 100)
                their_msg.rect.x, their_msg.rect.y = (100, 200)
            else:
                try:
                    # 3 lines of get_nowait() to make sure even the Queue() is full, only the last item is returned
                    their_msg.rect.x, their_msg.rect.y = self.connection.pos_recv.get_nowait()
                    their_msg.rect.x, their_msg.rect.y = self.connection.pos_recv.get_nowait()
                    their_msg.rect.x, their_msg.rect.y = self.connection.pos_recv.get_nowait()
                except queue.Empty:
                    pass
            my_msg.text = f"I'm at {str((my_msg.rect.x, my_msg.rect.x))}"
            self.connection.pos_send = my_msg.pos()
            their_msg.text = f"They are at {str((their_msg.rect.x, their_msg.rect.x))}"
            msg_grp.update()
            msg_grp.draw(self.screen)

            pygame.display.flip()

    def cb_dropselecton_onchange(self, item_index: tuple, game_ready, room_id):  # [[player0_name, game_ready, room_id],]
        self.chosen_room = room_id

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

        self.main_menu = pygame_menu.Menu(
            "Platform Game", WINDOW_SIZE[0] * 0.8, WINDOW_SIZE[1] * 0.8,
            center_content=False,
            onclose=pygame_menu.events.EXIT,  # User press ESC button
            theme=no_title_theme,
            position=[40, 30],
        )

        self.join_game_menu = pygame_menu.Menu(
            'Choosing Games', WINDOW_SIZE[0] * 0.8, WINDOW_SIZE[1] * 0.8,
            center_content=False,
            onclose=pygame_menu.events.EXIT,  # User press ESC button
            theme=no_title_theme_join_game,
            position=[40, 20],
        )

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

        b_connect = self.main_menu.add.button("Connection status: disconnected",
                                              self.conn_conn,
                                              server_ip.get_value(),
                                              server_port.get_value(),
                                              player_name.get_value())

        b_connect.add_self_to_kwargs()

        self.main_menu.add.button("Create a new game", self.set_create)

        self.selector_game = self.main_menu.add.dropselect(
            title='Choose a game to join:',
            items=self.game_rooms,
            selection_box_bgcolor=(200, 200, 50)
        )

        # choose_game = self.main_menu.add.button(self.room_selected1 + self.room_selected2, self.join_game_menu)

        self.join_game_menu.add.vertical_margin(30)

        refresh_frame = self.join_game_menu.add.frame_h(400, 50, padding=0, align=ALIGN_CENTER)

        b_refresh = self.join_game_menu.add.button("refresh",
                                                   self.refresh,
                                                   server_ip.get_value(),
                                                   server_port.get_value(),
                                                   player_name.get_value(),
                                                   font_color=(51, 94, 28),
                                                   background_color=(255, 221, 119),
                                                   selection_color=(249, 7, 7),
                                                   cursor=CURSOR_HAND)

        refresh_frame.pack(self.join_game_menu.add.label("Please"))
        refresh_frame.pack(b_refresh)
        refresh_frame.pack(self.join_game_menu.add.label(" the game list!"))

        self.join_game_menu.add.vertical_margin(10)

        self.room_frame = self.join_game_menu.add.frame_v(600, 1500,
                                                          background_color=(240, 230, 185),
                                                          padding=0,
                                                          max_width=600,
                                                          max_height=300,
                                                          align=ALIGN_CENTER)
        self.room_frame.set_title('Game Rooms', title_font_color=(247, 159, 7), padding_inner=(2, 5))

        # for i in range(100):
        #     self.room_frame.pack(self.join_game_menu.add.button("Empty room",
        #                                                         self.game_room_selected,
        #                                                         self.game_rooms[i][1],
        #                                                         font_color='red',
        #                                                         button_id=f'b{i}'), align=ALIGN_CENTER)

        # self.update_rooms()

        self.join_game_menu.add.vertical_margin(30)

        b_return = self.join_game_menu.add.button("Join",
                                                  self.join,
                                                  server_ip.get_value(),
                                                  server_port.get_value(),
                                                  player_name.get_value(),
                                                  font_color=(51, 94, 28),
                                                  background_color=(255, 221, 119),
                                                  selection_color=(249, 7, 7),
                                                  align=ALIGN_CENTER,
                                                  cursor=CURSOR_HAND)

        self.main_menu.add.button("Start",
                                  self.demo_game,
                                  server_ip.get_value(),
                                  server_port.get_value(),
                                  player_name.get_value())

        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)
        self.main_menu.add.vertical_margin(50)
        self.main_menu.add.label("Disclaimer: you agree to use this program on your own risks.",
                                 font_color="red",
                                 font_size=20,
                                 align=ALIGN_CENTER)
        self.main_menu.set_sound(all_sound, recursive=True)  # Apply on menu and all sub-menus

        # -------------------------------------------------------------------------
        # Main loop
        # -------------------------------------------------------------------------
        while True:
            self.clock.tick(FPS)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if self.main_menu.is_enabled():
                self.screen.blit(background_image, (0, 0))
                self.main_menu.update(events)
                if self.main_menu.is_enabled():
                    self.main_menu.draw(self.screen)
            else:
                break

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
