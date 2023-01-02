import pygame
import pygame_menu
from pygame_menu import themes
from time import sleep
import BlockKit


level = 1
GAME_COMPLETE_EVENT = pygame.USEREVENT + 1


def set_level(_, selected_level):
    global level
    level = selected_level


def start_the_game():
    max_level = 8
    for i in range(level, max_level+1):
        BlockKit.level_main(i)
    pygame.event.post(pygame.event.Event(GAME_COMPLETE_EVENT))


def main():
    pygame.init()
    surface = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Block Kit")
    width = 600
    height = 400
    WHITE = (255, 255, 255)
    mainmenu = pygame_menu.Menu('Block Kit', width, height, theme=themes.THEME_DARK)
    mainmenu.add.button('Play', start_the_game)
    mainmenu.add.selector('Level', [('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8)],
                          onchange=set_level, style='fancy', style_fancy_arrow_margin=(0, 0, 0),
                          style_fancy_bgcolor=(0, 0, 0, 0), style_fancy_bordercolor=(0, 0, 0, 0),
                          style_fancy_arrow_color=(0, 132, 201))
    mainmenu.add.button('Quit', pygame_menu.events.EXIT)
    arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15))
    screen = pygame.display.set_mode((width, height))
    cat_img = pygame.image.load('player.png')
    cat_xy = 400, 150
    block_img = pygame.image.load('block.jpg')
    block_img_scaled = pygame.transform.smoothscale(block_img, (50, 50))
    block_xy = 360, 330
    fatcat_img = pygame.image.load('fatcat_black.png')
    fatcat_img_scaled = pygame.transform.smoothscale(fatcat_img, (width, height))
    fatcat_xy = 0, 0

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == GAME_COMPLETE_EVENT:
                screen = pygame.display.set_mode((width, height))
                screen.fill(WHITE)
                screen.blit(fatcat_img_scaled, fatcat_xy)
                pygame.display.update()
                sleep(10)

        if mainmenu.is_enabled():
            mainmenu.update(events)
            mainmenu.draw(surface)
            if mainmenu.get_current().get_selected_widget():
                arrow.draw(surface, mainmenu.get_current().get_selected_widget())
            screen.blit(cat_img, cat_xy)
            screen.blit(block_img_scaled, block_xy)

        pygame.display.update()


if __name__ == "__main__":
    main()
