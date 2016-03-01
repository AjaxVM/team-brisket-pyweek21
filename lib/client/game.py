from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import pygame
from .. import settings
from ..shared import constants
from twisted.internet import reactor

log = logging.getLogger(__name__)


class Game(object):

    def __init__(self):

        self.game_client = None

        self.movement_actions = [
            constants.PLAYER_MOVE_RIGHT,
            constants.PLAYER_MOVE_LEFT,
            constants.PLAYER_MOVE_JUMP
        ]

    def setup(self, game_client):
        log.info('Initializing Game')
        self.game_client = game_client

        pygame.init()
        self.is_running = True
        self.screen = pygame.display.set_mode(settings.WINDOW_SIZE)
        pygame.display.set_caption(settings.GAME_TITLE)

    def destroy(self):
        log.info('Tearing down Game')
        if self.is_running:
            self.is_running = False
            pygame.quit()

    def doAction(self, action):
        if action in self.movement_actions:
            self.game_client.command(action)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_client.stop()
                return
            elif event.type == pygame.KEYDOWN:
                log.info('Got Key Event: '+str(event))
                if event.key == pygame.K_ESCAPE:
                    self.game_client.stop()
                    return

                elif event.key in settings.CONTROLS:
                    self.doAction(settings.CONTROLS[event.key])

    def render(self):
        self.screen.fill((0,0,0))

    def gameLoop(self):
        self.handleEvents()

        if not self.is_running:
            return #make sure we don't try to render again :O

        self.render()

        pygame.display.flip()
