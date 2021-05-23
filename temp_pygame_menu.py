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

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        onclose=pygame_menu.events.EXIT,  # User press ESC button
        theme=no_title_theme,
        title='Epic Menu',
        width=WINDOW_SIZE[0] * 0.8,
        columns=2,
        rows=10,
        position=[30, 80],
    )

    main_menu.add.text_input(
        'Server ip address: ',
        default='0.0.0.0',
        onreturn=None,
        textinput_id='server_ip'
    )

    main_menu.add.vertical_margin(30)

    main_menu.add.text_input(
        'Server port#: ',
        default='1111',
        onreturn=None,
        textinput_id='server_port'
    )

    main_menu.add.button("Create a new game", None)
    main_menu.add.button("Create a new game", None)
    main_menu.add.dropselect("Join a game: ", ["Room1", "Room2", "Room3"])

    widget_colors_theme = pygame_menu.themes.THEME_BLUE.copy()
    widget_colors_theme.widget_margin = (0, 10)
    widget_colors_theme.widget_padding = 0
    widget_colors_theme.widget_selection_effect.margin_xy(10, 5)
    widget_colors_theme.widget_font_size = 20
    widget_colors_theme.set_background_color_opacity(0.5)  # 50% opacity

    widget_colors = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        theme=widget_colors_theme,
        title='Widget backgrounds',
        width=WINDOW_SIZE[0] * 0.8
    )

    button_image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_CARBON_FIBER)

    widget_colors.add.button('Opaque color button',
                             background_color=(100, 100, 100))
    widget_colors.add.button('Transparent color button',
                             background_color=(50, 50, 50, 200), font_size=40)
    widget_colors.add.button('Transparent background inflate to selection effect',
                             background_color=(50, 50, 50, 200),
                             margin=(0, 15)).background_inflate_to_selection_effect()
    widget_colors.add.button('Background inflate + font background color',
                             background_color=(50, 50, 50, 200),
                             font_background_color=(200, 200, 200)
                             ).background_inflate_to_selection_effect()
    widget_colors.add.button('This inflates background to match selection effect',
                             background_color=button_image,
                             font_color=(255, 255, 255), font_size=15
                             ).selection_expand_background = True
    widget_colors.add.button('This is already inflated to match selection effect',
                             background_color=button_image,
                             font_color=(255, 255, 255), font_size=15
                             ).background_inflate_to_selection_effect()

    main_menu.add.button('Test different widget colors', widget_colors)
    main_menu.add.button('Another fancy button', lambda: print('This button has been pressed'))
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