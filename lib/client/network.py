from twisted.internet import protocol
from twisted.internet import reactor
from ..shared.protocol import JsonReceiver
from ..shared import constants
from .. import settings
from .game import Game
import pygame
import logging

log = logging.getLogger(__name__)

class GameClient(object):

    def __init__(self, game, factory):
        log.info('Setup GameClient')
        self.ticking = False
        self.client = None

        self.game = game
        self.game.setup(self)

        self.factory = factory

        self.connection = None

        self.fps = 1.0 / settings.FPS
        self.network_fps = 1.0 / settings.NETWORK_FPS

        self.command_queue = []

    def command(self, command, **kwargs):
        self.command_queue.append({
            'command': command,
            'kwargs': kwargs
        });

    def start(self):
        log.info('Started GameClient')
        self.ticking = True
        self.tick()
        self.eventTick()

    def stop(self):
        log.info('Stopping GameClient')
        self.disconnect()
        self.ticking = False
        self.game.destroy()
        reactor.stop()

    def connect(self):
        log.info('Connecting to server')
        self.connection = reactor.connectTCP('localhost', settings.DEFAULT_PORT, self.factory)

    def disconnect(self):
        log.info('Disconnecting from server')
        if self.connection:
            self.connection.disconnect()
            self.connection = None

    def setClient(self, client):
        self.client = client

    def processEvents(self):
        if self.command_queue:
            if self.client:
                self.client.sendCommand('commands', commands=self.command_queue)
            else:
                print 'WTF???'
            self.command_queue = []

    def tick(self):
        if self.ticking:
            self.game.gameLoop()
            reactor.callLater(self.fps, self.tick)

    def eventTick(self):
        if self.ticking:
            self.processEvents()
            reactor.callLater(self.network_fps, self.eventTick)

class ZombieClientProtocol(JsonReceiver):
    # todo: move all potential client and server 'directives' (commands) to constants
    # key_mapping = {
    #     constants.STATE_ACTION: {
    #         pygame.K_LEFT: 'left',
    #         pygame.K_RIGHT: 'right',
    #         pygame.K_z: 'jump',
    #         pygame.K_ESCAPE: 'quit',
    #     },
    #     constants.STATE_WAITING: {
    #         pygame.K_ESCAPE: 'quit',
    #     },
    # }

    def __init__(self, game_client):
        self.game_client = game_client #TODO: do we need access to this?
        self.connected = False

    def connectionMade(self):
        self.connected = True
        self.game_client.setClient(self)

    def sendCommand(self, command, **kwargs):
        self.sendObject(command=command, params=kwargs)


class ZombieClientFactory(protocol.ClientFactory):
    def __init__(self):
        game = Game()

        self.game_client = GameClient(game, self)
        self.game_client.start()

        self.game_client.connect()

    def buildProtocol(self, addr):
        p = ZombieClientProtocol(self.game_client)
        p.factory = self
        return p
    
