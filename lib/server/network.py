from __future__ import absolute_import, division, print_function, unicode_literals
from ..shared.protocol import JsonReceiver
from twisted.internet.protocol import Factory
import logging
import json
from .. import settings
from .game import GameServer

log = logging.getLogger(__name__)


class ZombieProtocol(JsonReceiver):
    """ Handles communication with one client """

    def __init__(self, game_server, router):
        self.game_server = game_server
        self.router = router
        self.slot = None

    def connectionMade(self):
        peer = self.transport.getPeer()
        try:
            self.slot = self.router.addPlayer(protocol=self)
        except ServerFull:
            log.error('Rejected {0}:{1} because server is full'.format(peer.host, peer.port))
            self.sendLine('No slots currently open on this server. Bye.')
            self.transport.loseConnection()
        self.game_server.playerJoin(self.slot)
        log.info("Connection made from {0}:{1} to slot {2}".format(peer.host, peer.port, self.slot))

    def connectionLost(self, reason=None):
        self.router.removePlayer(self.slot)
        peer = self.transport.getPeer()
        log.info("Connection lost from {0}:{1} to slot {2}".format(peer.host, peer.port, self.slot))

    def objectReceived(self, obj):
        log.debug(json.dumps(obj))
        move_actions = []
        for command in obj:
            if command['command'] == 'move':
                move_actions.append(command['action'])
        self.game_server.push_actions(self.slot, move_actions)
        

class ZombieFactory(Factory):
    """ Creates protocol objects """

    def __init__(self, game_server, router):
        self.game_server = game_server
        self.router = router

    def buildProtocol(self, addr):
        return ZombieProtocol(self.game_server, self.router)


class ZombieRouter(object):
    """ Keeps track of clients and lets the server message them """

    def __init__(self):
        self.clients = {}

    def addPlayer(self, protocol):
        try:
            slot = next(i for i in xrange(1, settings.NUMBER_OF_PLAYERS + 1) if i not in self.clients)
        except StopIteration:
            raise ServerFull()
        self.clients[slot] = protocol
        return slot

    def removePlayer(self, slot):
        self.clients.pop(slot, None)

    def sendTo(self, slot, obj):
        self.clients[slot].sendObject(obj)

    def broadcast(self, obj):
        for player in self.clients.values():
            player.sendObject(obj)

    def empty(self):
        return len(self.clients) == 0


class ServerFull(Exception):
    pass



def server_process():
    from twisted.internet import reactor
    log.debug('Twisted listening on port {}'.format(settings.DEFAULT_PORT))
    router = ZombieRouter()
    reactor.listenTCP(settings.DEFAULT_PORT, ZombieFactory(GameServer(router), router))
    reactor.run()
