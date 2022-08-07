import pygame as pg
import pygame_menu

from typing import Optional

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
FPS = 60
WINDOW_SIZE = (1024, 768)

sound: Optional['pygame_menu.sound.Sound'] = None
surface: Optional['pg.Surface'] = pg.image.load("resources\gui\Window_06.png")
main_menu: Optional['pygame_menu.Menu'] = None


class DrawText(pg.sprite.Sprite):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.font_name = "resources/OvOV20.ttf"
        self.font = pg.font.Font(self.font_name, 30)
        self.image = self.font.render(text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.speed = 3

    def update(self) -> None:
        self.image = self.font.render(self.text, True, (255, 255, 255))
        self.rect.x += self.speed
        if self.rect.x > WINDOW_SIZE[0]:
            self.rect.x = 0

    def chg_font(self, font_name):
        self.font_name = font_name
        self.font = pg.font.Font(self.font_name, 30)

    def chg_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Game:
    def __init__(self):
        pg.init()
        self.running = True
        self.playing = True
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.font_lst = pg.font.get_fonts()

    def new(self):
        self.font_cnt = 0
        self.text = DrawText("Example Text!")
        self.txt_grp = pg.sprite.Group()
        self.txt_grp.add(self.text)

    def run(self):
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.playing = False

    def update(self):
        self.txt_grp.update()

    def draw(self):
        self.screen.fill((125, 125, 125))
        self.txt_grp.draw(self.screen)

        pg.display.flip()

    def start_screen(self):
        self.new()

    def end_screen(self):
        pg.quit()
        exit()


g = Game()
g.start_screen()
while g.running:
    g.new()
    g.run()
    g.end_screen()