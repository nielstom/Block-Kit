import pygame

# Configurable Grid Size
NROWS = 25
NCOLS = 50

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)

BRICK = 1
BLOCK = 2
DOOR = 3
PLAYER = 4

# Cell Size
WIDTH = 10
HEIGHT = 10
MARGIN = 5
WINDOW_SIZE = [NCOLS*WIDTH*7/4, NROWS*HEIGHT*7/4]

grid = []
for row in range(NROWS):
    grid.append([])
    for column in range(NCOLS):
        grid[row].append(0)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Block-Kit - Level Generator")
done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            try:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                grid[row][column] += 1  # Increment object type
                if grid[row][column] > PLAYER:
                    grid[row][column] = 0

                min_row = 99999
                min_col = 99999
                for row in range(NROWS):
                    for column in range(NCOLS):
                        if grid[row][column] != 0:
                            min_row = min(min_row, row)
                            min_col = min(min_col, column)

                print("\n"*100)

                print("bricks_x = ", end="")
                for row in range(NROWS):
                    for column in range(NCOLS):
                        if grid[row][column] == BRICK:
                            print(column-min_col+1, end=", ")
                print("\b\b")
                print("bricks_y = ", end="")
                for row in range(NROWS):
                    for column in range(NCOLS):
                        if grid[row][column] == BRICK:
                            print(row-min_row+1, end=", ")
                print("\b\b")

                print("blocks_x = [", end="")
                for row in range(NROWS):
                    for column in range(NCOLS):
                        if grid[row][column] == BLOCK:
                            print(column-min_col+1, end=", ")
                print("\b\b]")
                print("blocks_y = [", end="")
                for row in range(NROWS):
                    for column in range(NCOLS):
                        if grid[row][column] == BLOCK:
                            print(row-min_row+1, end=", ")
                print("\b\b]")

                print("door_x = ", end="")
                for row in range(NROWS):
                    for column in range(NCOLS):
                        if grid[row][column] == DOOR:
                            print(column-min_col+1)
                print("door_y = ", end="")
                for row in range(NROWS):
                    for column in range(NCOLS):
                        if grid[row][column] == DOOR:
                            print(row-min_row+1)

                print("player_x = ", end="")
                for row in range(NROWS):
                    for column in range(NCOLS):
                        if grid[row][column] == PLAYER:
                            print(column-min_col+1)
                print("player_y = ", end="")
                for row in range(NROWS):
                    for column in range(NCOLS):
                        if grid[row][column] == PLAYER:
                            print(row-min_row+1)
            except:
                pass

    screen.fill(BLACK)
    for row in range(NROWS):
        for column in range(NCOLS):
            color = WHITE
            if grid[row][column] == BRICK:
                color = GRAY
            elif grid[row][column] == BLOCK:
                color = YELLOW
            elif grid[row][column] == DOOR:
                color = RED
            elif grid[row][column] == PLAYER:
                color = BLUE
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
