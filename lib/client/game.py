from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import pygame
from .. import settings
from ..shared import constants
from twisted.internet import reactor

from .states import main_menu, play_game

log = logging.getLogger(__name__)


class Game(object):

    def __init__(self):

        self.game_client = None

        self.states = {
            'main_menu': main_menu.State,
            'play_game': play_game.State
        }
        self.current_state = None
        self.state_obj = None

    def setup(self, game_client):
        log.info('Initializing Game')
        self.game_client = game_client

        pygame.init()
        self.is_running = True
        self.screen = pygame.display.set_mode(settings.WINDOW_SIZE)
        pygame.display.set_caption(settings.GAME_TITLE)

    def destroy(self):
        if self.is_running:
            log.info('Tearing down Game')
            self.is_running = False
            pygame.quit()

    def forceQuit(self):
        self.destroy()
        self.game_client.stop()

    def gotoState(self, state):
        if self.state_obj:
            self.state_obj.leave()
        self.current_state = state
        self.state_obj = self.states[self.current_state](self)

    def gameLoop(self):
        if not self.current_state:
            self.gotoState('main_menu')

        self.state_obj.handleEvents(pygame.event.get())

        if not self.is_running:
            return #make sure we don't try to render again :O

        self.screen.fill((0,0,0))

        self.state_obj.render()

        pygame.display.flip()
