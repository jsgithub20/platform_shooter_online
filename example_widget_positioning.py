"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - WIDGET POSITIONING
Test widget positioning example.
"""

import pygame_menu
from pygame_menu.examples import create_example_window

# Create the surface
surface = create_example_window('Example - Widget Positioning', (640, 480))

# Create a custom theme
my_theme = pygame_menu.themes.THEME_DARK.copy()
my_theme.title = False  # Hide the menu title

btn_unpressed_img = pygame_menu.BaseImage("resources/gui/right.png")
btn_pressed_img = pygame_menu.BaseImage("resources/gui/right_pressed.png")


# def cb_btn_pressed(selected, widget: pygame_menu.widgets.Button, ref_menu):
#     widget.set_background_color(btn_pressed_img)

def cb_btn_pressed(**kwargs):
    w = kwargs["widget"]
    w.set_background_color(btn_pressed_img)
    print(f"[{w.get_attribute('direction')}] button pressed")


def cb_btn_mouseleave(widget: pygame_menu.widgets.Button, event):
    widget.set_background_color(btn_unpressed_img)


menu = pygame_menu.Menu(
    height=480,  # Use full-screen
    theme=my_theme,
    title='',
    center_content=False,
    width=640
)

# menu.add.label(
#     'My App',
#     background_color='#333',
#     background_inflate=(30, 0),
#     float=True  # Widget does not add size to the menu
# ).translate(0, 10)
#
# label = menu.add.label(
#     'Lorem ipsum',
#     float=True,
#     font_name=pygame_menu.font.FONT_OPEN_SANS_ITALIC,
#     font_size=25)
# label.rotate(90)
# label.translate(300, 160)
#


# Button options
b1 = menu.add.button(
    '     ',
    lambda: print(f'My method'),
    align=pygame_menu.locals.ALIGN_LEFT,
    float=True,
    font_color=(0, 200, 0, 0),
    background_color=btn_unpressed_img
    # selection_color='#ff0'
)

b1._selected = False
b1.add_self_to_kwargs()
b1.set_onreturn(cb_btn_pressed)
b1.set_onmouseleave(cb_btn_mouseleave)
b1.set_attribute("direction", "r")

b1.translate(10, 170)
b2 = menu.add.button(
    'Exit',
    pygame_menu.events.EXIT,
    align=pygame_menu.locals.ALIGN_LEFT,
    float=True,
    selection_color='#fff'
)
b2.translate(10, 235)
#
# # Bottom scrollable text
# f = menu.add.frame_v(
#     background_color='#6b6e5e',
#     border_color='#36372f',
#     border_width=1,
#     float=True,
#     height=480,
#     max_height=100,
#     width=200
# )
# f.translate(220, 390)
# labels = [menu.add.label(f'  Lorem ipsum #{i}', font_size=15, font_color='#000000', padding=0) for i in range(20)]
# for j in labels:
#     f.pack(j)

if __name__ == '__main__':
    menu.mainloop(surface)
