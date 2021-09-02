import csv
import pygame as pg
from random import randint
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
        self.font = pg.font.Font(self.font_name, 50)
        self.image = self.font.render(text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.shadow = None

    def update(self) -> None:
        self.image = self.font.render(self.text, True, (255, 255, 255))

    def chg_font(self, font_name):
        self.font_name = font_name
        self.font = pg.font.SysFont(self.font_name, 50, bold=randint(0, 1), italic=randint(0, 1))
        if randint(0, 1):
            self.font.underline = True
        else:
            self.font.underline = False

    def chg_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def add_shadow(self):
        self.shadow = self.font.render(self.text, True, (100, 100, 100))
        self.shadow.blit(self.image, (-2, -2))
        self.image = self.shadow


class Game:
    def __init__(self):
        pg.init()
        self.running = True
        self.playing = True
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.sys_font = pg.font.get_fonts()
        self.next_font = ""

    def new(self):
        self.font_cnt = 210
        self.text = DrawText("Example Text!")
        self.txt_grp = pg.sprite.Group()
        self.txt_grp.add(self.text)
        self.font_lst = self.read_csv("font_lst.csv")
        self.run()

    def run(self):
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

        self.end_screen()

    def events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.playing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    try:
                        self.next_font = self.sys_font[self.font_cnt]
                        if self.font_cnt + 1 < len(self.sys_font):
                            self.font_cnt += 1
                        else:
                            # with open('new_font_lst.csv', 'w', newline='') as csvfile:
                            #     writer = csv.writer(csvfile)
                            #     writer.writerow(self.font_lst)
                            self.playing = False
                        if self.next_font in self.font_lst:
                            # print(self.next_font)
                            self.text.chg_font(self.next_font)
                    except:
                        self.text.chg_font(self.font_lst[0])
                # if event.key == pg.K_d:
                #     print(self.next_font + " is deleted")
                #     self.font_lst.remove(self.next_font)

    def update(self):
        self.txt_grp.update()

    def draw(self):
        self.screen.fill((166, 214, 201))
        self.txt_grp.draw(self.screen)

        pg.display.flip()

    def start_screen(self):
        self.new()

    def end_screen(self):
        pg.quit()
        exit()

    def read_csv(self, file_name):
        lst = []
        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for item in reader:
                lst.append(item[0])
        return lst


g = Game()
g.start_screen()
while g.running:
    g.new()
    g.run()
    g.end_screen()