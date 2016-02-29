from __future__ import absolute_import, division, print_function, unicode_literals
from ..shared.protocol import JsonReceiver
from twisted.internet.protocol import Factory
import logging
from .. import settings
from .game import GameServer

log = logging.getLogger(__name__)


class ZombieProtocol(JsonReceiver):

    def __init__(self, game_server, players):
        self.game_server = game_server
        self.players = players
        self.slot = None

    def connectionMade(self):
        peer = self.transport.getPeer()
        log.debug("Connection made from {0}:{1}".format(peer.host, peer.port))

        if len(self.players) >= settings.NUMBER_OF_PLAYERS:
            self.sendLine('No slots currently open on this server. Bye.')
            self.transport.loseConnection()

        self.slot = self.factory.addPlayer()
        log.info('Slot {0} is now occupied'.format(self.slot))
        
    def connectionLost(self, reason=None):
        if self.slot is not None:
            log.info('Slot {0} is now free'.format(self.slot))
        self.factory.removePlayer(self.slot)
        peer = self.transport.getPeer()
        log.debug("Connection lost from {0}:{1}".format(peer.host, peer.port))

    def objectReceived(self, obj):
        log.info('Server received: {0}'.format(obj))
        

class ZombieFactory(Factory):

    def __init__(self, game_server):
        self.game_server = game_server
        self.players = {}
                     
    def buildProtocol(self, addr):
        log.info('Remote addr: {}'.format(addr))
        p = ZombieProtocol(self.game_server, self.players)
        p.factory = self
        return p
        
    def addPlayer(self):
        slot = next(i for i in xrange(1, settings.NUMBER_OF_PLAYERS + 1) if i not in self.players)
        self.players[slot] = 1 #TODO - name players
        return slot
                    
                     
    def removePlayer(self, slot):
        self.players.pop(slot, None)
    
def server_process():
    from twisted.internet import reactor
    log.debug('Twisted listening on port {}'.format(settings.DEFAULT_PORT))
    reactor.listenTCP(settings.DEFAULT_PORT, ZombieFactory(GameServer()))
    reactor.run()
