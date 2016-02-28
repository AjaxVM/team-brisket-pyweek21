from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import subprocess
import pygame
from . import settings
from .client.game import Game

log = logging.getLogger(__name__)


def run_game():
    log.info('Starting server')
    server = subprocess.Popen('./run_server.py')
    try:
        log.info('Starting pygame')
        pygame.init()
        screen = pygame.display.set_mode(settings.WINDOW_SIZE)
        game = Game(screen)
        game.start()
        while game.is_running:
            game.tick()

    finally:
        server.terminate()  # not great longterm
