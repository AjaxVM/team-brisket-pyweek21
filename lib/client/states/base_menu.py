from __future__ import absolute_import, division, print_function, unicode_literals
import pygame
import os
from ...settings import DATA_DIR, GAME_TITLE


COLOR_TITLE = (244, 100, 70)


# Possibly duplicative but whatever, combine with asset loading later
class CrapLoader(dict):
    def __missing__(self, key):
        if key == 'menu_bg':
            bg = pygame.image.load(os.path.join(DATA_DIR, 'assets/menu.png')).convert()
            width, height = bg.get_size()
            bg = pygame.transform.scale(bg, (width * 5, height * 5))
            return bg
        elif key == 'menu_font':
            return pygame.font.Font(os.path.join(DATA_DIR, 'fonts/ShadowsIntoLight.ttf'), 50)

CRAP_LOADER = CrapLoader()


def render_menu_bg(screen):
    screen.blit(CRAP_LOADER['menu_bg'], (0, 0))
    outlined_text(screen, CRAP_LOADER['menu_font'], GAME_TITLE, COLOR_TITLE, 40, 10)


def outlined_text(screen, font, text, color, x, y):
    black = font.render(text, True, (0, 0, 0))
    for dx, dy in ((1, 1), (-1, -1), (1, -1), (-1, 1)):
        screen.blit(black, (x + dx, y + dy))
    screen.blit(font.render(text, True, color), (x, y))
