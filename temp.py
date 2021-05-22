import pygame.display
import pygame_menu
from pygame_menu.examples import create_example_window
from random import randrange
from typing import Tuple, Any

surface = create_example_window('Example - Simple', (600, 400))

items = [('Default', (255, 255, 255)),
         ('Black', (0, 0, 0)),
         ('Blue', (0, 0, 255)),
         ('Random', (-1, -1, -1))]

def set_difficulty(selected: Tuple, value: Any) -> None:
    """
    Set the difficulty of the game.
    :return: None
    """
    print('Set difficulty to {} ({})'.format(selected[0], value))


def start_the_game() -> None:
    """
    Function that starts a game. This is raised by the menu button,
    here menu can be disabled, etc.
    :return: None
    """
    global user_name
    print('{0}, Do the job here!'.format(user_name.get_value()))


def change_background_color(*args):
    # value_tuple, index = selected_value
    # print(f"value = {value_tuple}, index = {index}")
    # # print('Change widget color to', value_tuple[0])  # selected_value ('Color', surface, color)
    # if color == (-1, -1, -1):  # Generate a random color
    #     color = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
    # widget: 'pygame_menu.widgets.Selector' = kwargs.get('widget')
    # widget.update_font({'selected_color': color})
    # widget.get_selection_effect().color = color
    print(*args)
    # print(**kwargs)


menu = pygame_menu.Menu(
    height=300,
    theme=pygame_menu.themes.THEME_BLUE,
    title='Welcome',
    width=400
)
#
# user_name = menu.add.text_input('Name: ', default='John Doe', maxchar=10)
# menu.add.selector('Difficulty: ', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
# menu.add.button('Play', start_the_game)
# menu.add.button('Quit', pygame_menu.events.EXIT)

selector = menu.add.selector(
    title='Current color:\t',
    items=items,
    onreturn=change_background_color,  # User press "Return" button
    onchange=change_background_color  # User changes value with left/right keys
)
# selector.add_self_to_kwargs()  # Callbacks will receive widget as parameter
selector2 = menu.add.selector(
    title='New color:',
    items=items,
    style=pygame_menu.widgets.SELECTOR_STYLE_FANCY
)


if __name__ == '__main__':
    while True:
        menu.mainloop(surface)

        pygame.display.flip()





