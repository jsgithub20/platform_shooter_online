import pygame, pygame_menu
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()

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

items = [('Yes', 0),
         ('Absolutely Yes', 1)]

def call_back_print(widget):
    print(widget.title)

def call_back_select(selected, widget, menu):
    print(widget.get_title())

def cb_onchange(selectecd_ii, a):
    print(selectecd_ii[0])
    print(a)

menu = pygame_menu.Menu(
    'Choosing Games', 1024 * 0.8, 768 * 0.8,
    center_content=False,
    onclose=pygame_menu.events.EXIT,  # User press ESC button
    theme=no_title_theme_join_game,
    position=[40, 20])

selector_epic = menu.add.dropselect(
    title='Is pygame-menu epic?',
    items=items,
    font_size=16,
    selection_option_font_size=20
)
selector_sum = menu.add.dropselect(
    title='What is the value of π?',
    items=[('3 (Engineer)', 0),
           ('3.1415926535897932384626433832795028841971693993751058209', 1),
           ('4', 2),
           ('I don\'t know what is π', 3)],
    font_size=16,
    selection_box_width=173,
    selection_option_padding=(0, 5),
    selection_option_font_size=20
)
selector_country = menu.add.dropselect(
    title='Pick a country',
    items=[('Argentina', 'ar'),
           ('Australia', 'au'),
           ('Bolivia', 'bo'),
           ('Chile', 'ch'),
           ('China', 'cn'),
           ('Finland', 'fi'),
           ('France', 'fr'),
           ('Germany', 'de'),
           ('Italy', 'it'),
           ('Japan', 'jp'),
           ('Mexico', 'mx'),
           ('Peru', 'pe'),
           ('United States', 'us')],
    font_size=20,
    default=3,
    open_middle=True,  # Opens in the middle of the menu
    selection_box_height=5,
    selection_box_width=212,
    selection_infinite=True,
    selection_option_font_size=20,
    onchange=cb_onchange
)

while True:
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                items.append(['new item', 'new'])
                print(items)
                selector_epic.update_items(items)

    menu.update(events)
    menu.draw(screen)

    pygame.display.flip()