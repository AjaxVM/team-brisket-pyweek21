from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import pygame
from .. import settings

log = logging.getLogger(__name__)


class Game(object):

    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.Surface(settings.WINDOW_SIZE)
        self.is_running = True

    def start(self):
        self.background.fill(pygame.Color('#000000'))

    def tick(self):
        pygame.display.set_caption(settings.GAME_TITLE)
        self.screen.blit(self.background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                return
            elif event.type == pygame.KEYDOWN:
                log.debug('User pressed key: {} {}'.format(event.key, chr(event.key)))
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                    return
        pygame.display.update()
