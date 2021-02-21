"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

From:
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py

Explanation video: http://youtu.be/BCxWJgN4Nnc

Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/
"""

import pygame

# Global constants

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

class DrawText:
    def __init__(self, screen, size, color, x, y):
        self.screen = screen
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.font = pygame.font.Font("resources/You Blockhead.ttf", self.size)
        # self.font = pg.font.SysFont(None, self.size)

    def draw(self, text):
        text_surface = self.font.render(text, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.x, self.y)
        self.screen.blit(text_surface, text_rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction, screen_width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.direction = direction
        self.screen_width = screen_width
        self.live_flag = 1
        self.speed = 10
        self.loop_count = 0
        self.level = None
        if self.direction == 'l':
            self.speed = -self.speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = self.screen_width
            self.loop_count += 1
        if self.rect.x > self.screen_width:
            self.rect.x = 0
            self.loop_count += 1
        if self.loop_count == 2:
            self.live_flag = 0
        if pygame.sprite.spritecollide(self, self.level.platform_list, False):
            self.live_flag = 0


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        self.eye = pygame.Surface((20, 20))
        self.eye.fill(WHITE)
        self.image.blit(self.eye, (20, 0))

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None

        self.direction = 'r'

        self.hit_count = 0
        self.chop_count = 0
        self.jump_count = 0

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
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
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
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
        if self.rect.right > SCREEN_WIDTH:
            self.rect.left = 0

        # If the player gets near the left side, shift the world right (+x)
        if self.rect.left < 0:
            self.rect.right = SCREEN_WIDTH

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
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
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
        self.change_x = -6
        self.direction = 'l'
        color = self.image.get_at((self.rect.w-1, self.rect.h-1))
        self.image.fill(color)
        self.image.blit(self.eye, (0, 0))

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
        self.direction = 'r'
        color = self.image.get_at((self.rect.w-1, self.rect.h-1))
        self.image.fill(color)
        self.image.blit(self.eye, (20, 0))

    def stop(self):
        """ Called when the user lets off the keyboard. """
        if self.change_x > 0:
            self.direction = 'r'
        elif self.change_x < 0:
            self.direction = 'l'
        self.change_x = 0


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class Level:
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = None

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(BLUE)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform
        level = [[210, 30, 500, 500],
                 [210, 30, 200, 400],
                 [210, 30, 700, 300],
                 [210, 30, 200, 200],
                 [210, 30, 100, 100],
                 [210, 30, 600, 100],
                 [210, 30, 100, 500],
                 [210, 30, 50, 650],
                 [210, 30, 600, 650],
                 [100, 30, 0, 300],
                 [100, 30, 924, 500],
                 [100, 30, 400, 300],
                 [30, 30, 440, 270]
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Platformer Jumper")

    bullets = []

    # Create the player
    player_shooter = Player()
    player_chopper = Player()
    player_chopper.image.fill(WHITE)

    # Create all the levels
    level_list = []
    level_list.append(Level_01(player_shooter))
    level_list.append(Level_01(player_chopper))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    bullet_sprite_grp = pygame.sprite.Group()

    player_shooter.level = current_level
    player_shooter.rect.x = 200
    player_shooter.rect.y = 0

    player_chopper.level = current_level
    player_chopper.rect.x = 600
    player_chopper.rect.y = 200

    active_sprite_list.add(player_shooter, player_chopper)

    name_input = DrawText(screen, 30, WHITE, 100, 100)
    server_input = DrawText(screen, 30, WHITE, 150, 150)
    port_input = DrawText(screen, 30, WHITE, 200, 200)

    name_str = ""
    server_str = ""
    port_str = ""

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if 32 <= event.key <= 126:
                    print(event.unicode + ":" + str(event.key))
                # player_shooter controls
                if event.key == pygame.K_LEFT:
                    player_shooter.go_left()
                if event.key == pygame.K_RIGHT:
                    player_shooter.go_right()
                if event.key == pygame.K_UP:
                    player_shooter.jump()
                if event.key == pygame.K_SPACE:
                    if len(bullets) <= 5:
                        if player_shooter.direction == 'l':
                            bullet = Bullet(player_shooter.rect.x, player_shooter.rect.y, 'l', SCREEN_WIDTH)
                            bullet.level = current_level
                        else:
                            bullet = Bullet(player_shooter.rect.x, player_shooter.rect.y, 'r', SCREEN_WIDTH)
                            bullet.level = current_level
                        bullets.append(bullet)
                        for bullet in bullets:
                            bullet_sprite_grp.add(bullet)

                # player_chopper controls
                if event.key == pygame.K_a:
                    player_chopper.go_left()
                if event.key == pygame.K_d:
                    player_chopper.go_right()
                if event.key == pygame.K_w:
                    player_chopper.jump()

            if event.type == pygame.KEYUP:
                # player_shooter controls
                if event.key == pygame.K_LEFT and player_shooter.change_x < 0:
                    player_shooter.stop()
                if event.key == pygame.K_RIGHT and player_shooter.change_x > 0:
                    player_shooter.stop()

                # player_chopper controls
                if event.key == pygame.K_a and player_chopper.change_x < 0:
                    player_chopper.stop()
                if event.key == pygame.K_d and player_chopper.change_x > 0:
                    player_chopper.stop()

        # Update the player.
        active_sprite_list.update()
        bullet_sprite_grp.update()
        if player_chopper in active_sprite_list:
            bullet_hit_chopper = pygame.sprite.spritecollideany(player_chopper, bullet_sprite_grp)
            if bullet_hit_chopper:
                bullet_hit_chopper.live_flag = 0
                player_chopper.hit_count += 1
                if player_chopper.hit_count == 9:
                    active_sprite_list.remove(player_chopper)

            if pygame.sprite.collide_rect(player_shooter, player_chopper):
                player_shooter.chop_count += 1
                if player_shooter.chop_count > 60:
                    active_sprite_list.remove(player_shooter)

        if bullets:
            for bullet in bullets:
                if bullet.live_flag == 0:
                    bullet_sprite_grp.remove(bullet)
                    bullets.remove(bullet)

        # Update items in the level
        current_level.update()

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        bullet_sprite_grp.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


if __name__ == "__main__":
    main()