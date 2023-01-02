import pygame
from pygame.locals import *
import sys
import time

# TODO: Level Generator
# TODO: xml level parsing

BLOCK_SIZE = 60
WIDTH = 1300
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
        super().__init__("brick.png", startx, starty)


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
    pygame.init()

    WHITE = (255, 255, 255)
    FPS = 10
    FramePerSec = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Block Kit - Level " + str(level_number))

    doors = pygame.sprite.Group()
    bricks = pygame.sprite.Group()
    blocks = pygame.sprite.Group()

    # TODO: Read from configure file (fct of level_number) -------------------------------------
    player_x = 17
    player_y = 5
    door_x = 2
    door_y = 5
    bricks_x = 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 5, 5, 6, 7, 8, 9, 9, 10, 11, 12, 13, 13, 13, 14, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20
    bricks_y = 1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 5, 4, 6, 6, 6, 6, 5,  6,  6,  6,  6,  5,  4,  6,  6,  6,  6,  6,  6,  6,  5,  4,  3,  2,  1
    blocks_x = [11, 15]
    blocks_y = [5,   5]
    # Read and update WIDTH, HEIGHT, BLOCK_SIZE from config file
    # TODO: Read from configure file (fct of level_number) -------------------------------------

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
