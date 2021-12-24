import pygame, pygame_menu, asyncio
from pygame.locals import *
import role_def

pygame.init()
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()

background_image = pygame.image.load("resources\gui\Window_19_1024-768.png")
# background_image = pygame_menu.BaseImage("resources\gui\Window_19_1024-768.png")

girl_idle = []

for i in range(9):
    girl_idle.append(pygame.image.load(f"resources/gui/girl/Idle__00{i}.png"))

boy_idle = []

for i in range(9):
    boy_idle.append(pygame.image.load(f"resources/gui/boy/Idle__00{i}.png"))

img_lst = [girl_idle, boy_idle]

current_img_sel = 0
current_img_lst = img_lst[current_img_sel]

no_title_theme_join_game = pygame_menu.themes.THEME_ORANGE.copy()
no_title_theme_join_game.background_color = (0, 0, 0, 0)
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

sub_menu1_theme = pygame_menu.themes.THEME_ORANGE.copy()
sub_menu1_theme.background_color = (0, 0, 0, 0)
sub_menu1_theme.title_close_button = False
sub_menu1_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
sub_menu1_theme.title_offset = (200, 0)
sub_menu1_theme.title_font_shadow = True
sub_menu1_theme.title_font_color = (200, 50, 50)
sub_menu1_theme.widget_font = "resources/OvOV20.ttf"
sub_menu1_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
sub_menu1_theme.widget_padding = 5

items = [('Yes', 0),
         ('Absolutely Yes', 1)]


def cb_player_sel_lft():
    global current_img_sel
    global img_lst
    global current_img_lst
    global girl_desc_lbl_lst
    global boy_desc_lbl_lst
    if current_img_sel - 1 < 0:
        current_img_sel = len(img_lst) - 1
    else:
        current_img_sel -= 1

    if current_img_sel == 0:
        for j in range(len(girl_desc_lbl_lst)):
            girl_desc_lbl_lst[j].show()
            boy_desc_lbl_lst[j].hide()
    elif current_img_sel == 1:
        for j in range(len(girl_desc_lbl_lst)):
            girl_desc_lbl_lst[j].hide()
            boy_desc_lbl_lst[j].show()

    current_img_lst = img_lst[current_img_sel]

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

def cb_sub_menu_open(from_menu, to_menu):
    print("sub_menu opened")
    print(f"from menu: {from_menu.get_title()}")
    print(f"to menu: {to_menu.get_title()}")

async def add_item(widget_drop_select: pygame_menu.widgets.widget.dropselect):
    drop_items = widget_drop_select.get_items()
    print(drop_items)
    await asyncio.sleep(2)
    drop_items.append(("new item", 2))
    widget_drop_select.update_items(drop_items)
    print(drop_items)

def cb_get_text(txt):
    print(txt)

menu = pygame_menu.Menu(
    'Choosing Games', 1024 * 0.8, 768 * 0.8,
    center_content=False,
    onclose=pygame_menu.events.EXIT,  # User press ESC button
    theme=no_title_theme_join_game,
    position=[40, 20])

sub_menu = pygame_menu.Menu(
    'Choosing Games', 1024 * 0.8, 768 * 0.88,
    center_content=False,
    onclose=pygame_menu.events.EXIT,  # User press ESC button
    theme=sub_menu_theme,
    position=[40, 20])

sub_menu1 = pygame_menu.Menu(
    'Choosing Games', 1024, 768,
    center_content=False,
    onclose=pygame_menu.events.EXIT,  # User press ESC button
    theme=sub_menu1_theme,
    position=[40, 20])

sub_menu.add.button("button")

sub_menu.set_onbeforeopen(cb_sub_menu_open)

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
    default=0,
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
    # onselect=cb_onselect
)

txt = menu.add.text_input("Text Input: ", default="test", onreturn=None)
btn1 = menu.add.button("Get text", cb_get_text, txt.get_value())

menu.add.button("selection", sub_menu1)

lbl_match_type = sub_menu1.add.label("Match Types")
lbl_match_type.set_float(True, False, True)
lbl_match_type.translate(100, 60)

selector_match_type = sub_menu1.add.dropselect(
    title='',
    items=[("Deathmatch", 0),
           ("1st23", 1),
           ("Best of 3", 2)],
    font_size=26,
    selection_box_width=173,
    selection_box_height=100,
    selection_option_padding=(0, 5),
    selection_option_font_size=20
)
selector_match_type.set_float(True, False, True)
selector_match_type.translate(60, 100)

lbl_map = sub_menu1.add.label("Map Selection")
lbl_map.set_float(True, False, True)
lbl_map.translate(680, 60)

selector_map = sub_menu1.add.dropselect(
    title='',
    items=[("Map0", 0),
           ("Map1", 1),
           ("Map3", 2)],
    font_size=26,
    selection_box_width=173,
    selection_box_height=100,
    selection_option_padding=(0, 5),
    selection_option_font_size=20
)
selector_map.set_float(True, False, True)
selector_map.translate(650, 100)

btn_img_lft = pygame_menu.BaseImage("resources/gui/left.png")

# title text can't be empty, otherwise resize doesn't work!
sub1_btn_lft = sub_menu1.add.button(" ", cb_player_sel_lft, background_color=btn_img_lft)
sub1_btn_lft.resize(100, 100)
sub1_btn_lft.set_float(True, False, True)
sub1_btn_lft.translate(150, 200)

btn_img_rgt = pygame_menu.BaseImage("resources/gui/right.png")

sub1_btn_rgt = sub_menu1.add.button(" ", None, background_color=btn_img_rgt)
sub1_btn_rgt.resize(100, 100)
sub1_btn_rgt.set_float(True, False, True)
sub1_btn_rgt.translate(750, 200)

img = sub_menu1.add.surface(current_img_lst[0])
img.set_float(True, False, True)
img.translate(350, 100)

girl_desc_lbl_lst = []
for i in range(len(role_def.girl_txt)):
    lbl = sub_menu1.add.label(role_def.girl_txt[i][5], "",
                              font_size=role_def.girl_txt[i][0],
                              font_color=role_def.girl_txt[i][1])
    lbl.set_float(True, False, True)
    lbl.translate(role_def.girl_txt[i][2], role_def.girl_txt[i][3])
    girl_desc_lbl_lst.append(lbl)
boy_desc_lbl_lst = []
for i in range(len(role_def.boy_txt)):
    lbl = sub_menu1.add.label(role_def.boy_txt[i][5], "",
                              font_size=role_def.boy_txt[i][0],
                              font_color=role_def.boy_txt[i][1])
    lbl.set_float(True, False, True)
    lbl.translate(role_def.boy_txt[i][2], role_def.boy_txt[i][3])
    lbl.hide()
    boy_desc_lbl_lst.append(lbl)

img_idx = 0
current_img_idx = 0

while True:
    clock.tick(60)

    screen.blit(background_image, (0, 0))
    # background_image.draw(screen)

    events = pygame.event.get()
    for event in events:
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if len(items) < 3:
                    items.append(['new item', 'new'])
                else:
                    del items[-1]
                selector_epic.update_items(items)
                selector_epic.render()

    if img_idx + 1 == len(current_img_lst) * 2:
        img_idx = 0
    else:
        img_idx += 1

    if img_idx//2 != current_img_idx:
        img.set_surface(current_img_lst[img_idx//2])

    menu.update(events)
    menu.draw(screen)

    pygame.display.flip()
