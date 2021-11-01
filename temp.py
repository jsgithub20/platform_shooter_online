import pygame, pygame_menu, asyncio
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()

no_title_theme_join_game = pygame_menu.themes.THEME_ORANGE.copy()
no_title_theme_join_game.background_color = (123, 123, 123)
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

sub_menu_theme = pygame_menu.themes.THEME_ORANGE.copy()
sub_menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT

items = [('Yes', 0),
         ('Absolutely Yes', 1)]

def cb_onselect(selected, widget, menu):
    if selected:
        print("selected")
    else:
        print("not selected")

def cb_onchange(selectecd_ii: tuple, a):
    print(selectecd_ii)
    print(a)

def cb_btn():
    print("test btn pressed")


async def add_item(widget_drop_select: pygame_menu.widgets.widget.dropselect):
    drop_items = widget_drop_select.get_items()
    print(drop_items)
    await asyncio.sleep(2)
    drop_items.append(("new item", 2))
    widget_drop_select.update_items(drop_items)
    print(drop_items)

menu = pygame_menu.Menu(
    'Choosing Games', 1024 * 0.8, 768 * 0.8,
    center_content=False,
    onclose=pygame_menu.events.EXIT,  # User press ESC button
    theme=no_title_theme_join_game,
    position=[40, 20])

sub_menu = pygame_menu.Menu(
    'Choosing Games', 1024 * 0.8, 768 * 0.8,
    center_content=False,
    onclose=pygame_menu.events.EXIT,  # User press ESC button
    theme=sub_menu_theme,
    position=[40, 20])

sub_menu.add.button("button")

ds = sub_menu.add.dropselect(
    title='Choose a game to join:',
    items=[("No game", False, 1), ],
    onchange=cb_onchange,
    selection_box_bgcolor=(200, 200, 50)
    )

menu.add.button("test", sub_menu)

selector_epic = menu.add.dropselect(
    title='Is pygame-menu epic?',
    items=items,
    font_size=16,
    selection_option_font_size=20,
)

selector_epic.add_self_to_kwargs()

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
selector_country = sub_menu.add.dropselect(
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
    # open_middle=True,  # Opens in the middle of the menu
    selection_box_height=5,
    selection_box_width=212,
    selection_infinite=True,
    selection_option_font_size=20,
    onchange=cb_onchange,
    onselect=cb_onselect
)

while True:
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if len(items) < 3:
                    items.append(['new item', 'new'])
                else:
                    del items[-1]
                print(items)
                selector_epic.update_items(items)
                selector_epic.render()

    menu.update(events)
    menu.draw(screen)

    pygame.display.flip()
