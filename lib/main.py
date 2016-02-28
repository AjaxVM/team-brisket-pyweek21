from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import pygame
from . import settings
from .client.game import Game

log = logging.getLogger(__file__)


def run_game():
    log.info('Starting pygame')
    pygame.init()
    screen = pygame.display.set_mode(settings.WINDOW_SIZE)
    game = Game(screen)
    game.start()
    while game.is_running:
        game.tick()


def run_server():
    log.info('Starting server')
    #TODO

    #for now just gonna test out the level loader
    from .server.level_loader import LevelLoader

    level = LevelLoader('level1')
