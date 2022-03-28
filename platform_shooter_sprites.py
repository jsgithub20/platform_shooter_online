import pygame
import pygame as pg
import pygame.freetype as ft
from ipaddress import ip_address
from platform_shooter_settings import *

# images for player_shooter
# Run animation for the RIGHT
run_R = [pg.image.load("resources/shooter/Run__000.png"), pg.image.load("resources/shooter/Run__001.png"),
         pg.image.load("resources/shooter/Run__002.png"), pg.image.load("resources/shooter/Run__003.png"),
         pg.image.load("resources/shooter/Run__004.png"), pg.image.load("resources/shooter/Run__005.png"),
         pg.image.load("resources/shooter/Run__006.png"), pg.image.load("resources/shooter/Run__007.png"),
         pg.image.load("resources/shooter/Run__008.png"), pg.image.load("resources/shooter/Run__009.png")]

# Run animation for the LEFT
run_L = [pg.transform.flip(sprite, True, False) for sprite in run_R]

# Attack animation for the RIGHT
attack_R = [pg.image.load("resources/shooter/Throw__000.png"), pg.image.load("resources/shooter/Throw__001.png"),
            pg.image.load("resources/shooter/Throw__002.png"), pg.image.load("resources/shooter/Throw__003.png"),
            pg.image.load("resources/shooter/Throw__004.png"), pg.image.load("resources/shooter/Throw__005.png"),
            pg.image.load("resources/shooter/Throw__006.png"), pg.image.load("resources/shooter/Throw__007.png"),
            pg.image.load("resources/shooter/Throw__008.png"), pg.image.load("resources/shooter/Throw__009.png")]

# Attack animation for the LEFT
attack_L = [pg.transform.flip(sprite, True, False) for sprite in attack_R]

img_dict = {"run_R": run_R, "run_L": run_L, "attack_R": attack_R, "attack_L": attack_L}

# tiles of the platforms
blocks = [pg.image.load("resources/platform/13.png"),
          pg.image.load("resources/platform/14.png"),
          pg.image.load("resources/platform/15.png")]

long_block = pg.Surface([210, 40], pg.SRCALPHA)
long_block.blit(blocks[0], (0, 0))
long_block.blit(blocks[1], (70, 0))
long_block.blit(blocks[2], (140, 0))

crate = pg.image.load("resources/platform/Crate.png")

idle_girl = [pg.image.load("resources/gui/girl/Idle__000.png"), pg.image.load("resources/gui/girl/Idle__001.png"),
             pg.image.load("resources/gui/girl/Idle__002.png"), pg.image.load("resources/gui/girl/Idle__003.png"),
             pg.image.load("resources/gui/girl/Idle__004.png"), pg.image.load("resources/gui/girl/Idle__005.png"),
             pg.image.load("resources/gui/girl/Idle__006.png"), pg.image.load("resources/gui/girl/Idle__007.png"),
             pg.image.load("resources/gui/girl/Idle__008.png"), pg.image.load("resources/gui/girl/Idle__009.png")]

idle_boy = [pg.image.load("resources/gui/boy/Idle__000.png"), pg.image.load("resources/gui/boy/Idle__001.png"),
             pg.image.load("resources/gui/boy/Idle__002.png"), pg.image.load("resources/gui/boy/Idle__003.png"),
             pg.image.load("resources/gui/boy/Idle__004.png"), pg.image.load("resources/gui/boy/Idle__005.png"),
             pg.image.load("resources/gui/boy/Idle__006.png"), pg.image.load("resources/gui/boy/Idle__007.png"),
             pg.image.load("resources/gui/boy/Idle__008.png"), pg.image.load("resources/gui/boy/Idle__009.png")]


class Buttons(pg.sprite.Sprite):
    def __init__(self, file, pos_x, pos_y, name):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.btn_clicked = 0
        self.name = name


class HealthBar(pg.sprite.Sprite):
    def __init__(self, x, y, health):
        pg.sprite.Sprite.__init__(self)
        self.full_length = 200
        self.bar_width = 5
        self.image = pygame.Surface((self.full_length, self.bar_width))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.x, self.y = (x, y)
        self.rect.x, self.y = (self.x, self.y)
        self.health = health
        self.hit = 0
        self.red_surface = pygame.Surface((self.hit * (self.full_length / self.health), self.bar_width))

    def update(self) -> None:
        self.red_surface = pygame.Surface((self.hit*(self.full_length/self.health), self.bar_width))
        self.red_surface.fill((255, 0, 0))
        self.image.blit(self.red_surface, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (self.x, self.y)

class DrawText(pg.sprite.Sprite):
    def __init__(self, screen, size, color, x, y, name, text, click=0, max_letter=0, valid_letters=None,
                 alignment=None):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.description = text
        self.input_text = ""
        self.text = self.description
        # self.font = pg.font.Font("resources/You Blockhead.ttf", self.size)
        # self.font = pg.font.Font("resources/OvOV20.ttf", self.size)
        self.font = ft.Font("resources/OvOV20.ttf", self.size)
        self.font.antialiased = True

        # self.image = self.font.render(text, True, color)
        self.image = self.font.render(text, color)[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (self.x, self.y)

        self.alignment = alignment

        """
        alignment is calculated in __init__() and update() twice so that some text that don't need
        update can also be placed at the right location       
        """
        if self.alignment == "left":
            self.rect.x = 10
        elif self.alignment == "center":
            self.rect.midtop = (self.screen_rect.center[0], self.y)
        elif self.alignment == "right":
            self.rect.x = self.screen_rect.w - self.rect.w - 10

        # if click = 1, mouse-clicking this text item leads to an action, otherwise it doesn't
        self.click = click

        # set to 1 if this text is clicked
        self.cursor = 0

        # set the flag to 1 if the cursor is on
        self.cursor_flag = 0
        self.name = name

        # max = max number of letters that can be accepted by self.input_text, used to avoid long text out of screen
        self.max = max_letter
        self.valid_letters = valid_letters

    def update(self):
        if self.click == 1:
            if self.cursor == 1:
                if self.cursor_flag == 0:
                    self.cursor_flag = 1
                    self.input_text += "_"
                    self.text = self.description + self.input_text
            elif self.cursor == 0:
                if self.cursor_flag == 1:
                    self.cursor_flag = 0
                    self.input_text = self.input_text[:-1]
                    self.text = self.description + self.input_text

        self.image = self.font.render(self.text, self.color)[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (self.x, self.y)

        if self.alignment == "left":
            self.rect.x = 10
        elif self.alignment == "center":
            self.rect.midtop = (self.screen_rect.center[0], self.y)
        elif self.alignment == "right":
            self.rect.x = self.screen_rect.w - self.rect.w - 10

    def add_letter(self, letter):
        if self.cursor == 1 and len(self.text) <= self.max:
            if self.valid_letters is not None:
                # key.unicode recieved from keybaord is "str" already
                if letter in self.valid_letters:
                    self.input_text = self.input_text[:-1] + letter + "_"
                    self.text = self.description + self.input_text
            else:
                self.input_text = self.input_text[:-1] + letter + "_"
                self.text = self.description + self.input_text

    def back_space(self):
        if self.cursor == 1:
            if len(self.input_text) > 1:
                self.input_text = self.input_text[:-2] + "_"
                self.text = self.description + self.input_text
            else:
                self.input_text = "_"
                self.text = self.description + self.input_text

    def finish(self):
        # remove the cursor "_" at the end of the text
        if self.cursor == 1:
            self.text = self.text[:-1]

    def check_ip(self):
        try:
            ip_address(self.input_text)
        except ValueError:
            self.draw_box((700, 170), WHITE, (180, 280))
            self.warning_msg("Invalid IP, stupid!", (250, 300))
            self.warning_msg("Press any key to continue", (200, 370))
            return "stop"

    def check_port(self):
        # port# should be > 2 digits
        if len(self.input_text) < 2:
            self.draw_box((700, 170), WHITE, (180, 280))
            self.warning_msg("Invalid port#, stupid!", (250, 300))
            self.warning_msg("Press any key to continue", (200, 370))
            return "stop"

    def check_name(self):
        if len(self.input_text) < 2:
            self.draw_box((700, 170), WHITE, (180, 280))
            self.warning_msg("Name yourself, stupid!", (250, 300))
            self.warning_msg("Press any key to continue", (200, 370))
            return "stop"

    def draw_box(self, size_xy, color, pos_xy):
        box = pg.Surface(size_xy)
        box.fill(color)
        shadow = pg.Surface(size_xy)
        shadow.fill((128, 128, 128))
        self.screen.blit(shadow, (pos_xy[0]+5, pos_xy[1]+5))
        self.screen.blit(box, pos_xy)
        pg.display.flip()

    def warning_msg(self, msg, pos_xy):
        # pos_xy format should be (pos_x, pos_y)
        warning = self.font.render(msg, True, RED)[0]
        self.screen.blit(warning, pos_xy)
        pg.display.flip()


class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, direction, screen_width):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("resources/shooter/spear_head.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.direction = direction
        self.screen_width = screen_width
        self.live_flag = 0
        self.speed = 10
        self.loop_count = 0
        self.level = None
        if self.direction == 'l':
            self.image = pg.transform.flip(self.image, True, False)
            self.speed = -self.speed

    def update(self):
        self.rect.x += self.speed
        if -50 < self.rect.x < 0:  # to avoid counting the bullets at (-99, -99)
            self.rect.x = self.screen_width
            self.loop_count += 1
        if self.rect.x > self.screen_width:
            self.rect.x = 0
            self.loop_count += 1
        if self.loop_count == 2:
            self.live_flag = 0
            self.loop_count = 0
        if pg.sprite.spritecollide(self, self.level.platform_list, False):
            self.live_flag = 0


class PlayerIdle(pg.sprite.Sprite):
    # parameter of pos_xy should be given in the form of (x, y), including the parenthesis
    def __init__(self, img_list, pos_xy):
        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.img_lst = img_list
        self.image_idx = 0
        self.image = self.img_lst[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        self.rect.x = pos_xy[0]
        self.rect.y = pos_xy[1]

    def chg_frame(self):
        # reduce frame change rate by changing frame when image_idx is increase by n (>1)
        if self.image_idx + 1 == len(self.img_lst)*3:
            self.image_idx = 0
        else:
            self.image_idx += 1
        self.image = self.img_lst[self.image_idx//3]

    def update(self):
        self.chg_frame()


class Player(pg.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # use a dict to store the images for different actions so that only the numbers need to be transferred from
        # server to the client
        self.image_idx = 0
        self.img_dict_key = "run_R"
        self.image = img_dict[self.img_dict_key][0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
        self.speed = 6

        # List of sprites we can bump against
        self.level = None

        self.direction = 'r'

        # counts of the player being hit
        self.hit_count = 0

        # set to 1 if the player is being hit, e.g. being chopped - which needs multiple sprite image flow
        self.hit_flag = 0
        self.jump_count = 0

        # number of hit for the player to be killed
        self.hit_limit = 0
        self.score_text = None

        # number of bullets that can be shot before reload
        self.loaded = 5

        # number of seconds before the player can shoot more bullets
        self.reload_timer = 0

        # set to 1 if the player is attacking, so the image set is changed to attacking sets
        self.attack_flg = 0

        self.keys = "000000000000"

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        if self.attack_flg == 1:
            self.chg_frame("attack_L")
        else:
            if self.change_x < 0:
                self.chg_frame("run_L")
            elif self.change_x > 0:
                self.chg_frame("run_R")

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

        self.reloading()

    def reloading(self):
        if self.loaded <= 0:
            if self.reload_timer == 0:
                self.reload_timer = pg.time.get_ticks()
            elif pg.time.get_ticks() - self.reload_timer >= 4000:
                self.loaded = 5
                self.reload_timer = 0

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

    def chg_frame(self, img_dict_key):
        self.img_dict_key = img_dict_key
        if self.attack_flg == 1:
            if self.direction == 'l':
                self.img_dict_key = "attack_L"
            elif self.direction == "r":
                self.img_dict_key = "attack_R"
        if self.image_idx + 1 == len(img_dict[img_dict_key]):
            self.image_idx = 0
            if self.attack_flg == 1:
                self.attack_flg = 0
        else:
            self.image_idx += 1

        img_list = img_dict[self.img_dict_key]
        self.image = img_list[self.image_idx]

    def update_img(self, img_dict_key, image_idx):
        img_list = img_dict[img_dict_key]
        self.image = img_list[image_idx]


class Platform(pg.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, block, pos_x, pos_y):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
        self.image = block

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y


class MovingPlatform(Platform):
    """ This is a fancier platform that can actually move. """
    def __init__(self, block, pos_x, pos_y, player_grp):
        super().__init__(block, pos_x, pos_y)
        self.change_x = 0
        self.change_y = 1

        self.boundary_top = 100
        self.boundary_bottom = 570
        self.boundary_left = 0
        self.boundary_right = 0

        self.level = None
        self.player_grp = player_grp

    def update(self):
        """ Move the platform. This update has to be called after the player update.
            basically, the update() for any moving parts has to be called one after the other.
            If the player is in the way, it will shove the player
            out of the way. This does NOT handle what happens if a
            platform shoves a player into another object. Make sure
            moving platforms have clearance to push the player around
            or add code to handle what happens if they don't. """

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit the player
        hit = pg.sprite.spritecollide(self, self.player_grp, False)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # If we are moving right, set our right side
            # to the left side of the item we hit
            for player in hit:
                if self.change_x < 0:
                    player.rect.right = self.rect.left
                else:
                    # Otherwise if we are moving left, do the opposite.
                    player.rect.left = self.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we the player
        hit = pg.sprite.spritecollide(self, self.player_grp, False)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # Reset our position based on the top/bottom of the object.
            for player in hit:
                if self.change_y < 0:
                    player.rect.bottom = self.rect.top
                else:
                    player.rect.top = self.rect.bottom

        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        # cur_pos = self.rect.x - self.level.world_shift
        # if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
        #     self.change_x *= -1


class Level:
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, background=None):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pg.sprite.Group()
        self.enemy_list = pg.sprite.Group()
        self.player_list = pg.sprite.Group()

        # Background image
        # self.background = pg.image.load("resources/platform/Tree_1024_768.png").convert_alpha()
        self.background = pg.image.load("resources/platform/angry_owl.png").convert_alpha()
        # self.background = background

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.blit(self.background, (0, 0))
        # screen.fill(LIGHT_BLUE)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player1, player2, background=None):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, background)
        self.player_list.add(player1, player2)


        # Array with width, height, x, and y of platform
        level = [[500, 500],
                 [200, 400],
                 [700, 300],
                 [200, 200],
                 [100, 100],
                 [600, 100],
                 [100, 500],
                 [50, 650],
                 [600, 650],
                 [0, 300],
                 [400, 300],
                 [440, 270]
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(long_block, platform[0], platform[1])
            # block.player = self.player
            self.platform_list.add(block)


class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player1, player2, background=None):
        """ Create level 2. """

        # Call the parent constructor
        Level.__init__(self, background)
        self.player_list.add(player1, player2)
        self.moving_block = None

        # Array with x, and y of platform
        level = [[600, 500],
                 [200, 400],
                 [700, 300],
                 [200, 200],
                 [100, 100],
                 [600, 100],
                 [100, 500],
                 [50, 650],
                 [750, 650],
                 [400, 650],
                 [0, 300],
                 [924, 500],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(long_block, platform[0], platform[1])
            # block.player = self.player
            self.platform_list.add(block)

        # .convert_alpha() can only be used in a method of a class here, otherwise
        # the error "cannot convert without pygame.display initialized" will occur when this module is imported
        # to "main.py". The reason being the method in a class is only executed when the instance of a class is
        # created, but the lines out of the methods of a class will be executed when this module is imported
        self.moving_block = MovingPlatform(crate, 470, 300, self.player_list)
        self.platform_list.add(self.moving_block)