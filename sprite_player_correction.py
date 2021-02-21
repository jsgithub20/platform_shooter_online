"""
This sprite class is used when different image sizes are used for different movement, and when self.rect.x needs to be
shifted due to the different image sizes, for example, the image for chopping action has the player figure shifted in
the rect to allow room for the sword.
"""

import pygame as pg
from platform_shooter_settings import *

# images for player_chopper
# Run animation for the RIGHT
run_R = [pg.image.load("resources/chopper/Run__000.png"), pg.image.load("resources/chopper/Run__001.png"),
         pg.image.load("resources/chopper/Run__002.png"), pg.image.load("resources/chopper/Run__003.png"),
         pg.image.load("resources/chopper/Run__004.png"), pg.image.load("resources/chopper/Run__005.png"),
         pg.image.load("resources/chopper/Run__006.png"), pg.image.load("resources/chopper/Run__007.png"),
         pg.image.load("resources/chopper/Run__008.png"), pg.image.load("resources/chopper/Run__009.png")]

# Run animation for the LEFT
run_L = [pg.transform.flip(sprite, True, False) for sprite in run_R]

# Attack animation for the RIGHT
attack_R = [pg.image.load("resources/chopper/Attack__000.png"), pg.image.load("resources/chopper/Attack__001.png"),
         pg.image.load("resources/chopper/Attack__002.png"), pg.image.load("resources/chopper/Attack__003.png"),
         pg.image.load("resources/chopper/Attack__004.png"), pg.image.load("resources/chopper/Attack__005.png"),
         pg.image.load("resources/chopper/Attack__006.png"), pg.image.load("resources/chopper/Attack__007.png"),
         pg.image.load("resources/chopper/Attack__008.png"), pg.image.load("resources/chopper/Attack__009.png")]

# Attack animation for the LEFT
attack_L = [pg.transform.flip(sprite, True, False) for sprite in attack_R]


class Player(pg.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image_idx = 0
        self.image = run_R[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
        self.speed = 6

        # List of sprites we can bump against
        self.level = None

        self.direction = 'r'

        self.hit_count = 0
        self.hit_flag = 0
        self.jump_count = 0
        self.hit_limit = 0
        self.score_text = None
        self.loaded = 5
        self.reload_timer = 0
        self.chop_flag = 0

        # x coordinate correction due to different width of the sprite
        # attack frame is 14 pixel wider than run frames for "ninjagirl" set, need to be corrected when attacking to
        # the left side
        self.x_correction = 14
        self.x_correction_flg = 0

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        if self.chop_flag == 1:
            self.chg_frame(attack_L)
        else:
            if self.change_x < 0:
                self.chg_frame(run_L)
            elif self.change_x > 0:
                self.chg_frame(run_R)

        if self.hit_flag == 1:
            self.hit_flag = 0

        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pg.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pg.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.jump_count = 0
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

        # If the player gets near the right side, shift the world left (-x)
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0

        # If the player gets near the left side, shift the world right (+x)
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            # self.change_y = 0
            self.jump_count = 0
            # self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.rect.y =  0

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pg.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # check whether it's double jump
        self.jump_count += 1

        # If it is ok to jump, set our speed upwards
        # if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT or self.jump_count <= 2:
        if self.jump_count <= 1:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -self.speed
        self.direction = 'l'

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = self.speed
        self.direction = 'r'

    def stop(self):
        """ Called when the user lets off the keyboard. """
        if self.change_x > 0:
            self.direction = 'r'
        elif self.change_x < 0:
            self.direction = 'l'
        self.change_x = 0

    def chop(self):
        self.chop_flag = 1

    def x_correction_on(self):
        self.rect.x -= self.x_correction
        self.x_correction_flg = 1

    def x_correction_off(self):
        self.rect.x += self.x_correction
        self.x_correction_flg = 0

    def chg_frame(self, img_list):
        if self.chop_flag == 1:
            if self.direction == 'l':
                img_list = attack_L
                # attack frame is 14 pixel wider than run frames for "ninjagirl" set
                if self.x_correction_flg == 0:
                    self.x_correction_on()
            elif self.direction == "r":
                img_list = attack_R
                if self.x_correction_flg == 1:
                    self.x_correction_off()
        elif self.chop_flag == 0 and self.x_correction_flg == 1:
            self.x_correction_off()
        if self.image_idx + 1 == len(img_list):
            self.image_idx = 0
            if self.chop_flag == 1:
                self.chop_flag = 0
        else:
            self.image_idx += 1

        current_pos = self.rect.x, self.rect.y
        self.image = img_list[self.image_idx]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = current_pos
