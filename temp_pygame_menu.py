import queue

import pygame
from threading import Thread
import pygame_menu
from pygame_menu.examples import create_example_window

from typing import Optional

import asyncio
import demo_async_client


# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
FPS = 60
WINDOW_SIZE = (1024, 768)

sound: Optional['pygame_menu.sound.Sound'] = None
surface: Optional['pygame.Surface'] = pygame.image.load("resources\gui\Window_06.png")
main_menu: Optional['pygame_menu.Menu'] = None

pygame.init()
clock = pygame.time.Clock()

# -----------------------------------------------------------------------------
# Load image
# -----------------------------------------------------------------------------
background_image = pygame_menu.BaseImage(
    image_path="resources\gui\Window_06.png"
)


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

    def update(self) -> None:
        self.image = self.font.render(self.text, True, (255, 255, 255))


class EventLoop(Thread):
    def __init__(self):
        self._loop = asyncio.get_event_loop()
        super().__init__(target=self._loop.run_forever)
        self.start()
        self.game_task = None

    def stop(self):
        self._loop.call_soon_threadsafe(self._loop.stop)

    def create_task(self, coro):
        self.game_task = asyncio.run_coroutine_threadsafe(coro, self._loop)


t_loop = EventLoop()


def start_game(server_ip, server_port):
    global main_menu
    connection = demo_async_client.Network(server_ip, server_port)
    t_loop.create_task(connection.start())
    main_menu.disable()

    global surface
    server_msg = DrawText("Server msg:")
    msg_grp = pygame.sprite.Group()
    msg_grp.add(server_msg)
    while True:
        clock.tick(60)
        surface.fill((0, 200, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                t_loop.game_task.cancel()
                t_loop.stop()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    t_loop.game_task.cancel()
                    t_loop.stop()
                    pygame.quit()
                    exit()
                if event.key == pygame.K_SPACE:
                    connection.pos_send[0] += 1
                    connection.pos_send[1] += 1

        if connection.server_msg != "Game Ready":
            server_msg.rect.x, server_msg.rect.y = (100, 100)
        else:
            try:
                # 3 lines of get_nowait() to make sure even the Queue() is full, only the last item is returned
                server_msg.rect.x, server_msg.rect.y = connection.pos_recv.get_nowait()
                server_msg.rect.x, server_msg.rect.y = connection.pos_recv.get_nowait()
                server_msg.rect.x, server_msg.rect.y = connection.pos_recv.get_nowait()
            except queue.Empty:
                pass
        server_msg.text = str((server_msg.rect.x, server_msg.rect.x))
        msg_grp.update()
        msg_grp.draw(surface)

        pygame.display.flip()

def main_background() -> None:
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    :return: None
    """
    background_image.draw(surface)


def game_window():
    global surface
    while True:
        clock.tick(60)
        surface.fill((0, 200, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                t_loop.game_task.cancel()
                t_loop.stop()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        pygame.draw.circle(surface, (255, 255, 255), (100, 100), 10.0)

        pygame.display.flip()


def main(test: bool = False) -> None:
    """
    Main program.
    :param test: Indicate function is being tested
    :return: None
    """

    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global main_menu
    # global sound
    global surface


    # -------------------------------------------------------------------------
    # Create window
    # -------------------------------------------------------------------------
    surface = create_example_window('Example - Image Background', WINDOW_SIZE)

    all_sound = pygame_menu.sound.Sound()
    # engine.set_sound(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, 'resources/sound/Designer_Stubble.ogg', volume=0.5)
    all_sound.set_sound(pygame_menu.sound.SOUND_TYPE_OPEN_MENU, 'resources/sound/Amazon.ogg', volume=0.5)
    # all_sound.play_open_menu()
    # engine.play_click_mouse()

    # -------------------------------------------------------------------------
    # Create menus: Main menu
    # -------------------------------------------------------------------------
    no_title_theme = pygame_menu.themes.THEME_ORANGE.copy()
    no_title_theme.background_color = (0, 0, 0, 50)
    # no_title_theme.title = False
    no_title_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
    no_title_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
    no_title_theme.widget_padding = 5

    no_title_theme_join_game = pygame_menu.themes.THEME_ORANGE.copy()
    no_title_theme_join_game.background_color = (0, 0, 0, 50)
    # no_title_theme.title = False
    no_title_theme_join_game.widget_alignment = pygame_menu.locals.ALIGN_CENTER
    no_title_theme_join_game.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
    no_title_theme_join_game.widget_padding = 5

    main_menu = pygame_menu.Menu(
        '', WINDOW_SIZE[0] * 0.8, WINDOW_SIZE[1] * 0.7,
        center_content=False,
        onclose=pygame_menu.events.EXIT,  # User press ESC button
        theme=no_title_theme,
        position=[30, 80],
    )

    join_game_menu = pygame_menu.Menu(
        '', WINDOW_SIZE[0] * 0.8, WINDOW_SIZE[1] * 0.7,
        center_content=False,
        onclose=pygame_menu.events.EXIT,  # User press ESC button
        theme=no_title_theme_join_game,
        position=[30, 80],
    )

    main_menu.add.vertical_margin(10)

    server_ip = main_menu.add.text_input(
        'Server ip address: ',
        default='127.0.0.1',
        onreturn=None,
        textinput_id='server_ip',
        )

    server_port = main_menu.add.text_input(
        'Server port#: ',
        default='8888',
        onreturn=None,
        textinput_id='server_port'
        )

    main_menu.add.text_input(
        'Create a new game with name: ',
        default="Amy's game",
        onreturn=None,
        textinput_id='new_game'
    )

    main_menu.add.button('Join an existing game', join_game_menu)

    join_game_menu.add.button("Amy's Game")
    join_game_menu.add.button("John's Game")
    join_game_menu.add.button("Dora's Game")

    main_menu.add.button("Start the game",
                         lambda: start_game(server_ip.get_value(), server_port.get_value()))

    main_menu.add.button('Quit', pygame_menu.events.EXIT)
    main_menu.set_sound(all_sound, recursive=True)  # Apply on menu and all sub-menus

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            if event.type == pygame.QUIT:
                exit()

        if main_menu.is_enabled():
            main_background()
            main_menu.update(events)
            if main_menu.is_enabled():
                main_menu.draw(surface)
        else:
            break

        # Main menu
        # main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
    # game_window()
    pygame.quit()