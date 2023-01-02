import pygame
from pygame.locals import *
import sys
import time

BLOCK_SIZE = 60
WIDTH = 1200
HEIGHT = 600
PLACE_EVENT = pygame.USEREVENT + 1
PICKUP_EVENT = pygame.USEREVENT + 2
RESTART_EVENT = pygame.USEREVENT + 3


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()
        orig_image = pygame.image.load(image)
        self.image = pygame.transform.smoothscale(orig_image, (BLOCK_SIZE, BLOCK_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = [startx*BLOCK_SIZE, starty*BLOCK_SIZE]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, dx, dy, objects):
        # Checks collision (move, check, move-back)
        self.rect.move_ip([dx, dy])
        collide = pygame.sprite.spritecollideany(self, objects)
        self.rect.move_ip([-dx, -dy])
        return collide

    def apply_gravity(self, bricks_and_blocks):
        # Adjust y to the first collision
        dy = BLOCK_SIZE
        while not self.check_collision(0, dy, bricks_and_blocks):
            self.rect.move_ip([0, dy])


class Brick(Sprite):
    def __init__(self, startx, starty):
        super().__init__("brick.jpg", startx, starty)


class Block(Sprite):
    def __init__(self, startx, starty):
        super().__init__("block.jpg", startx, starty)


class Door(Sprite):
    def __init__(self, startx, starty):
        super().__init__("door.jpg", startx, starty)


class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("player.png", startx, starty)
        self.image = pygame.transform.flip(self.image, True, False)
        block_image_orig = pygame.image.load("block.jpg")
        self.block_image = pygame.transform.smoothscale(block_image_orig, (BLOCK_SIZE, BLOCK_SIZE))
        self.facing_left = False
        self.holding_box = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.holding_box:
            dy = -BLOCK_SIZE
            self.rect.move_ip([0, dy])
            screen.blit(self.block_image, self.rect)
            self.rect.move_ip([0, -dy])

    def update_image(self):
        orig_image = pygame.image.load("player.png")
        self.image = pygame.transform.scale(orig_image, (BLOCK_SIZE, BLOCK_SIZE))
        if not self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def end_of_level_check(self, doors):
        return pygame.sprite.spritecollideany(self, doors)

    def update(self, blocks, bricks_and_blocks):
        INPUT_DELAY = 0.1
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT] or pressed_keys[K_RIGHT]:  # Move Left/Right
            time.sleep(INPUT_DELAY)
            dx = BLOCK_SIZE*(1 - 2*pressed_keys[K_LEFT])
            if not self.check_collision(dx, 0, bricks_and_blocks):
                if (not self.holding_box) or (not self.check_collision(dx, -BLOCK_SIZE, bricks_and_blocks)):
                    self.rect.move_ip([dx, 0])
                    self.apply_gravity(bricks_and_blocks)
            self.facing_left = pressed_keys[K_LEFT]
            self.update_image()

        if pressed_keys[K_UP]:  # Climb
            time.sleep(INPUT_DELAY)
            dx = BLOCK_SIZE*(1 - 2*self.facing_left)
            dy = -BLOCK_SIZE
            if self.check_collision(dx, 0, bricks_and_blocks):
                if not self.check_collision(dx, dy, bricks_and_blocks):
                    if not self.check_collision(0, dy, bricks_and_blocks):
                        if (not self.holding_box) or (not self.check_collision(dx, dy-BLOCK_SIZE, bricks_and_blocks) and not self.check_collision(0, dy-BLOCK_SIZE, bricks_and_blocks)):
                            self.rect.move_ip([dx, dy])

        if pressed_keys[K_SPACE]:  # Pickup/Place
            time.sleep(INPUT_DELAY)
            dx = BLOCK_SIZE*(1 - 2*self.facing_left)
            if self.holding_box:  # Place
                if not self.check_collision(dx, -BLOCK_SIZE, bricks_and_blocks):
                    self.holding_box = False
                    pygame.event.post(pygame.event.Event(PLACE_EVENT))
            else:  # Pickup
                if self.check_collision(dx, 0, blocks):
                    if not self.check_collision(dx, -BLOCK_SIZE, bricks_and_blocks):
                        if not self.check_collision(0, -BLOCK_SIZE, bricks_and_blocks):
                            self.holding_box = True
                            pygame.event.post(pygame.event.Event(PICKUP_EVENT))

        if pressed_keys[K_ESCAPE]:  # Restart Level
            pygame.event.post(pygame.event.Event(RESTART_EVENT))


def level_main(level_number):
    global WIDTH, HEIGHT, BLOCK_SIZE
    # Note: Object locations generated by running "LevelGenerator.py" and copying its output here
    #       BLOCK_SIZE, WIDTH, HEIGHT manually tuned to best fit in frame
    # TODO: Check output on different screen resolutions (currently valid for 3840x2160)
    # TODO: Can this be compiled into an exe application?
    if level_number == 1:
        BLOCK_SIZE = 65
        WIDTH = 1400
        HEIGHT = 600
        bricks_x = 1, 20, 1, 20, 1, 20, 1, 20, 1, 5, 13, 20, 1, 5, 9, 13, 20, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
        bricks_y = 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7
        blocks_x = [11, 15]
        blocks_y = [6, 6]
        door_x = 2
        door_y = 6
        player_x = 17
        player_y = 6
    elif level_number == 2:
        BLOCK_SIZE = 55
        WIDTH = 1300
        HEIGHT = 600
        bricks_x = 2, 7, 8, 17, 18, 2, 19, 1, 2, 20, 1, 21, 1, 2, 22, 2, 14, 22, 2, 14, 22, 2, 3, 4, 5, 6, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 6, 10, 6, 7, 8, 9, 10
        bricks_y = 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 10, 10, 10, 10, 10
        blocks_x = [17, 15, 17, 18, 9]
        blocks_y = [6, 7, 7, 7, 9]
        door_x = 2
        door_y = 4
        player_x = 19
        player_y = 7
    elif level_number == 3:
        BLOCK_SIZE = 55
        WIDTH = 1100
        HEIGHT = 600
        bricks_x = 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 1, 3, 5, 19, 1, 4, 19, 1, 19, 1, 19, 1, 3, 4, 5, 14, 17, 18, 1, 3, 5, 10, 13, 14, 15, 16, 17, 1, 3, 5, 9, 10, 13, 1, 3, 5, 6, 7, 8, 9, 10, 12, 13, 1, 2, 3, 5, 6, 10, 11, 12
        bricks_y = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10
        blocks_x = [18, 17, 18, 15, 6, 7]
        blocks_y = [4, 5, 5, 6, 8, 8]
        door_x = 2
        door_y = 9
        player_x = 10
        player_y = 6
    elif level_number == 4:
        BLOCK_SIZE = 35
        WIDTH = 900
        HEIGHT = 600
        bricks_x = 19, 18, 20, 8, 17, 21, 7, 9, 16, 22, 4, 5, 6, 10, 15, 23, 3, 11, 14, 24, 2, 12, 13, 24, 2, 24, 2, 24, 2, 22, 23, 24, 1, 2, 7, 18, 22, 1, 7, 18, 19, 20, 21, 22, 1, 2, 3, 4, 5, 7, 16, 17, 18, 5, 7, 11, 13, 16, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 5, 6, 7
        bricks_y = 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 16, 16, 16
        blocks_x = [23, 22, 23, 9, 9, 13, 9, 14]
        blocks_y = [8, 9, 9, 12, 13, 13, 14, 14]
        door_x = 2
        door_y = 12
        player_x = 18
        player_y = 10
    elif level_number == 5:
        BLOCK_SIZE = 40
        WIDTH = 920
        HEIGHT = 600
        bricks_x = 6, 7, 8, 13, 14, 15, 16, 17, 18, 19, 20, 21, 2, 3, 4, 5, 9, 10, 11, 12, 22, 1, 22, 1, 22, 1, 22, 1, 7, 22, 1, 7, 22, 1, 7, 22, 1, 6, 7, 8, 9, 10, 11, 12, 22, 1, 2, 4, 5, 6, 12, 13, 15, 22, 2, 4, 13, 15, 16, 22, 2, 4, 13, 15, 16, 22, 2, 3, 4, 13, 15, 16, 17, 18, 19, 20, 21, 22, 13, 14, 15
        bricks_y = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14
        blocks_x = [8, 9, 10, 11, 21, 20, 21, 19, 20, 21]
        blocks_y = [8, 8, 8, 8, 10, 11, 11, 12, 12, 12]
        door_x = 2
        door_y = 9
        player_x = 13
        player_y = 9
    elif level_number == 6:
        BLOCK_SIZE = 42
        WIDTH = 940
        HEIGHT = 600
        bricks_x = 2, 3, 4, 18, 19, 20, 21, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 1, 2, 21, 1, 21, 1, 2, 21, 2, 21, 2, 13, 19, 20, 21, 2, 13, 19, 2, 13, 14, 15, 16, 17, 19, 2, 3, 4, 5, 6, 11, 12, 13, 17, 18, 19, 6, 11, 6, 7, 9, 10, 11, 7, 8, 9
        bricks_y = 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 12, 12, 12, 12, 12, 13, 13, 13
        blocks_x = [19, 20, 3, 4, 16, 3, 4, 5, 15, 16, 17, 3, 4, 5, 6, 10]
        blocks_y = [6, 6, 7, 7, 7, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 11]
        door_x = 2
        door_y = 4
        player_x = 14
        player_y = 8
    elif level_number == 7:
        BLOCK_SIZE = 40
        WIDTH = 1000
        HEIGHT = 600
        bricks_x = 3, 7, 8, 9, 10, 11, 15, 16, 20, 21, 22, 2, 4, 6, 12, 14, 17, 19, 23, 2, 5, 6, 13, 14, 18, 19, 24, 2, 6, 14, 19, 24, 2, 24, 2, 24, 1, 2, 24, 1, 22, 23, 24, 1, 2, 6, 14, 19, 20, 22, 2, 6, 13, 14, 19, 20, 21, 22, 2, 3, 6, 13, 14, 19, 3, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 3, 4, 6, 11, 12, 13, 4, 5, 6
        bricks_y = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 14, 14, 14
        blocks_x = [23, 23, 22, 23, 6, 8, 8, 16, 8, 9, 10, 16, 17, 18]
        blocks_y = [5, 6, 7, 7, 8, 9, 10, 10, 11, 11, 11, 11, 11, 11]
        door_x = 2
        door_y = 8
        player_x = 18
        player_y = 10
    elif level_number == 8:
        BLOCK_SIZE = 33
        WIDTH = 1100
        HEIGHT = 600
        bricks_x = 2, 3, 4, 12, 13, 14, 15, 19, 20, 21, 22, 23, 24, 25, 1, 5, 11, 16, 18, 26, 1, 6, 10, 16, 17, 27, 1, 7, 8, 9, 16, 22, 23, 24, 27, 1, 21, 22, 24, 27, 2, 3, 4, 24, 27, 4, 5, 18, 19, 24, 25, 27, 3, 10, 17, 20, 27, 3, 9, 11, 16, 20, 27, 2, 6, 7, 8, 12, 17, 20, 27, 2, 9, 11, 18, 19, 27, 1, 10, 22, 23, 24, 25, 26, 27, 1, 27, 1, 13, 14, 15, 27, 1, 5, 6, 7, 27, 1, 27, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
        bricks_y = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12, 13, 13, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 16, 16, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17
        blocks_x = [2, 2, 3, 8, 8, 26, 25, 26, 14, 6, 26, 25, 26, 10, 18, 24, 25, 26]
        blocks_y = [4, 5, 5, 8, 9, 10, 11, 11, 13, 14, 14, 15, 15, 16, 16, 16, 16, 16]
        door_x = 25
        door_y = 6
        player_x = 21
        player_y = 16
    elif level_number == 9:
        BLOCK_SIZE = 35
        WIDTH = 800
        HEIGHT = 600
        bricks_x = 9, 10, 11, 8, 12, 7, 13, 16, 17, 18, 19, 20, 6, 14, 15, 20, 5, 20, 4, 20, 3, 11, 12, 13, 20, 2, 17, 18, 19, 20, 1, 20, 1, 14, 15, 16, 20, 1, 2, 7, 8, 12, 20, 2, 7, 8, 12, 13, 17, 18, 19, 20, 2, 7, 8, 9, 10, 11, 12, 13, 16, 17, 2, 3, 4, 7, 13, 15, 16, 4, 6, 7, 13, 14, 15, 4, 5, 6
        bricks_y = 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 15, 16, 16, 16
        blocks_x = [11, 11, 12, 19, 18, 19, 15, 19, 9]
        blocks_y = [5, 6, 6, 6, 7, 7, 9, 11, 12]
        door_x = 2
        door_y = 10
        player_x = 15
        player_y = 8
    elif level_number == 10:
        BLOCK_SIZE = 30
        WIDTH = 900
        HEIGHT = 600
        bricks_x = 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 2, 3, 15, 25, 1, 2, 3, 4, 15, 25, 26, 1, 4, 5, 8, 12, 13, 14, 15, 16, 20, 21, 22, 24, 25, 27, 1, 5, 8, 9, 18, 19, 20, 22, 23, 24, 27, 1, 5, 6, 9, 10, 27, 1, 10, 11, 12, 13, 14, 15, 16, 27, 1, 2, 11, 15, 16, 17, 26, 27, 2, 12, 14, 17, 18, 27, 2, 8, 13, 18, 19, 27, 2, 3, 4, 5, 8, 9, 23, 24, 25, 26, 27, 4, 5, 6, 7, 8, 27, 4, 15, 27, 4, 14, 15, 20, 21, 22, 23, 24, 25, 26, 27, 4, 13, 14, 26, 4, 26, 4, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 26, 4, 9, 10, 20, 21, 26, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25, 26
        bricks_y = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 15, 15, 15, 15, 16, 16, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 18, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19
        blocks_x = [5, 13, 14, 16, 20, 21, 22, 24, 19, 11, 12, 13, 14, 8, 15, 25, 5, 24, 25, 5, 6, 23, 24, 25]
        blocks_y = [3, 3, 3, 3, 3, 3, 3, 3, 4, 6, 6, 6, 6, 9, 16, 16, 17, 17, 17, 18, 18, 18, 18, 18]
        door_x = 2
        door_y = 7
        player_x = 15
        player_y = 12
    elif level_number == 11:
        BLOCK_SIZE = 30
        WIDTH = 900
        HEIGHT = 600
        bricks_x = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 1, 4, 8, 29, 1, 8, 23, 24, 25, 26, 27, 29, 1, 6, 7, 8, 11, 12, 21, 22, 27, 29, 1, 8, 9, 10, 25, 27, 29, 1, 2, 3, 8, 14, 27, 29, 1, 5, 6, 7, 8, 15, 18, 19, 20, 24, 25, 26, 29, 1, 15, 17, 24, 29, 1, 11, 12, 13, 15, 17, 23, 26, 27, 28, 29, 1, 2, 3, 4, 10, 11, 12, 15, 17, 18, 22, 26, 29, 1, 15, 16, 17, 21, 25, 29, 1, 14, 18, 19, 20, 21, 29, 1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 23, 24, 25, 26, 27, 29, 1, 21, 22, 27, 29, 1, 2, 3, 4, 20, 27, 29, 1, 3, 4, 8, 13, 24, 25, 26, 27, 29, 1, 2, 4, 5, 6, 8, 13, 29, 1, 3, 5, 7, 8, 13, 29, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29
        bricks_y = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 17, 17, 17, 17, 17, 17, 17, 17, 18, 18, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19
        blocks_x = [7, 9, 10, 2, 10, 18, 2, 3, 17, 6, 7, 16, 2, 27, 2, 3, 18, 6, 19, 24, 13, 20, 5, 11, 12, 16, 20, 16, 25, 26, 17, 18, 19, 21, 22, 23, 24]
        blocks_y = [3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 12, 12, 12, 14, 14, 15, 15, 15, 17, 17, 17, 17, 18, 18, 18]
        door_x = 25
        door_y = 4
        player_x = 14
        player_y = 5
    else:
        return

    pygame.init()
    WHITE = (255, 255, 255)
    FPS = 10
    FramePerSec = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Block Kit - Level " + str(level_number))

    doors = pygame.sprite.Group()
    bricks = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    player = Player(player_x, player_y)
    doors.add(Door(door_x, door_y))
    for i in range(len(bricks_x)):
        bricks.add(Brick(bricks_x[i], bricks_y[i]))
    for i in range(len(blocks_x)):
        blocks.add(Block(blocks_x[i], blocks_y[i]))
    bricks_and_blocks = pygame.sprite.Group()
    bricks_and_blocks.add(bricks)
    bricks_and_blocks.add(blocks)

    while not player.end_of_level_check(doors):
        player.update(blocks, bricks_and_blocks)
        for event in pygame.event.get():
            if event.type == PLACE_EVENT:
                # Place block in front of player (1 tile above player then apply gravity)
                dx = BLOCK_SIZE*(1 - 2*player.facing_left)
                x = player.rect.centerx + dx
                dy = -BLOCK_SIZE
                y = player.rect.centery + dy
                b = Block(x/BLOCK_SIZE, y/BLOCK_SIZE)
                b.apply_gravity(bricks_and_blocks)
                blocks.add(b)
                bricks_and_blocks.add(b)
                blocks_x.append(b.rect.centerx/BLOCK_SIZE)
                blocks_y.append(b.rect.centery/BLOCK_SIZE)

            if event.type == PICKUP_EVENT:
                # Remove the pickup block (Reset blocks, bricks_and_blocks groups and omit by location)
                for entity in blocks:
                    entity.kill()
                dx = BLOCK_SIZE*(1 - 2*player.facing_left)
                for i in range(len(blocks_x)):
                    if player.rect.centerx+dx == blocks_x[i]*BLOCK_SIZE and player.rect.centery == blocks_y[i]*BLOCK_SIZE:
                        del blocks_x[i]
                        del blocks_y[i]
                        break
                for i in range(len(blocks_x)):
                    blocks.add(Block(blocks_x[i], blocks_y[i]))
                bricks_and_blocks.add(blocks)

            if event.type == RESTART_EVENT:
                # Restart level
                level_main(level_number)
                return

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        player.draw(screen)
        bricks_and_blocks.draw(screen)
        doors.draw(screen)
        pygame.display.update()
        FramePerSec.tick(FPS)
