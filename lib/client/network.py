from twisted.internet import protocol
from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet.task import deferLater
from ..shared.protocol import JsonReceiver
from .. import settings
from .game import Game
import logging

from multiprocessing import Process
from ..server.network import server_process

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

    def connect(self, host='localhost'):
        log.info('Connecting to server')
        self.connection = reactor.connectTCP(host, settings.DEFAULT_PORT, self.factory)

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
                log.warn('Not connected to server')
            self.command_queue = []

    def tick(self):
        if self.ticking:
            self.game.gameLoop()
            deferLater(reactor, self.fps, self.tick).addErrback(self.errorHandler)

    def eventTick(self):
        if self.ticking:
            self.processEvents()
            deferLater(reactor, self.network_fps, self.eventTick).addErrback(self.errorHandler)

    def errorHandler(self, failure):
        import traceback
        log.error('Quitting due to exception:\n{}'.format(traceback.format_exc(failure.value)))
        self.stop()


class ZombieClientProtocol(JsonReceiver):

    def __init__(self, game_client):
        self.game_client = game_client
        self.connected = False

    def connectionMade(self):
        self.connected = True
        self.game_client.setClient(self)

    def sendCommand(self, command, **kwargs):
        self.sendObject(command=command, params=kwargs)

    def objectReceived(self, obj):
        print(obj)


class ZombieClientFactory(protocol.ClientFactory):
    def __init__(self):
        game = Game()
        self.game_client = GameClient(game, self)
        self.game_client.start()
        reactor.run()

    def buildProtocol(self, addr):
        p = ZombieClientProtocol(self.game_client)
        p.factory = self
        return p
