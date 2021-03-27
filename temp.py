# state0 = {"player_id": 0, "role": "shooter", "pos_x": 0, "pos_y": 0, "img_dict_key": "1", "img_idx": 0}
# state1 = {"player_id": 1, "role": "chopper", "pos_x": 0, "pos_y": 0, "img_dict_key": "1", "img_idx": 0}
# state = {}
# state = {**state0, **state1}
# print(state)

# profile = {"role0": "self.roles[0]", "pos0_x": 0, "pos0_y": 0, "img_dict_key0": "", "img_idx0": 0}
# ext_info = {"role1": "self.roles[1]", "pos1_x": 0, "pos1_y": 0, "img_dict_key1": "", "img_idx1": 0}
# full_profile01 = {**profile, **ext_info}
# print(full_profile01)

import pygame as pg

run_R = [pg.image.load("resources/shooter/Run__000.png"), pg.image.load("resources/shooter/Run__001.png"),
         pg.image.load("resources/shooter/Run__002.png"), pg.image.load("resources/shooter/Run__003.png"),
         pg.image.load("resources/shooter/Run__004.png"), pg.image.load("resources/shooter/Run__005.png"),
         pg.image.load("resources/shooter/Run__006.png"), pg.image.load("resources/shooter/Run__007.png"),
         pg.image.load("resources/shooter/Run__008.png"), pg.image.load("resources/shooter/Run__009.png")]

pg.init()


class Test(pg.sprite.Sprite):
    def __init__(self, step):
        super().__init__()
        self.image = run_R[0]
        self.rect = self.image.get_rect()
        self.step = step
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        self.rect.x += self.step
        self.rect.y += self.step


clock = pg.time.Clock()
test1 = Test(1)
test2 = Test(2)
test_sprites = pg.sprite.Group()
test_sprites.add(test1, test2)

while True:
    clock.tick(60)
    test_sprites.update()
    if pg.sprite.collide_rect(test1, test2):
        print("collided")
    else:
        print("no collision")
