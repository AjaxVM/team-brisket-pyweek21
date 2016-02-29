from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import pygame
from .. import settings
from .network import ZombieClientFactory
from ..shared import constants
from twisted.internet import reactor

log = logging.getLogger(__name__)


class Game(object):

    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.Surface(settings.WINDOW_SIZE)
        self.is_running = True
        self.state = constants.STATE_ACTION  #todo actually implement state

    def connect(self, host, port):
        self.factory = ZombieClientFactory(self)
        reactor.connectTCP(host, port, self.factory)
        reactor.run()

    def start(self):
        self.background.fill(pygame.Color('#000000'))
        reactor.callLater(0.1, self.tick)

    def tick(self):
        pygame.display.set_caption(settings.GAME_TITLE)
        self.screen.blit(self.background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                    return
                self.userInputReceived(event.key)
        pygame.display.update()
        if self.is_running:
            reactor.callLater(0.1, self.tick)

    def bindToClient(self, userInputReceived):
        self.userInputReceived = userInputReceived
