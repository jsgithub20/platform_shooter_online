import pygame
import pygame_menu
from pygame_menu.examples import create_example_window

from typing import Optional


# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
FPS = 60
WINDOW_SIZE = (1024, 768)

sound: Optional['pygame_menu.sound.Sound'] = None
surface: Optional['pygame.Surface'] = pygame.image.load("resources\gui\Window_06.png")
main_menu: Optional['pygame_menu.Menu'] = None

pygame.init()

# -----------------------------------------------------------------------------
# Load image
# -----------------------------------------------------------------------------
background_image = pygame_menu.BaseImage(
    image_path="resources\gui\Window_06.png"
)


# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def main_background() -> None:
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    :return: None
    """
    background_image.draw(surface)


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
    clock = pygame.time.Clock()

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
        default='0.0.0.0',
        onreturn=None,
        textinput_id='server_ip',
        )

    server_port = main_menu.add.text_input(
        'Server port#: ',
        default='1111',
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
                         lambda: print(f"server address: {server_ip.get_value()}:{server_port.get_value()}"))

    main_menu.add.button('Quit', pygame_menu.events.EXIT)
    main_menu.set_sound(all_sound, recursive=True)  # Apply on menu and all sub-menus

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        # events = pygame.event.get()
        # for event in events:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         pass
        #
        #     if main_menu.is_enabled():
        #         main_background()
        #         main_menu.update(events)
        #         main_menu.draw(surface)

        # Main menu
        main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()