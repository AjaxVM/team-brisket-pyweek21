from __future__ import absolute_import, division, print_function, unicode_literals
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
import logging
from .. import settings

log = logging.getLogger(__name__)


class ZombieProtocol(LineReceiver):

    def __init__(self):
        pass

    def connectionMade(self):
        log.debug("Protocol connected")

    def connectionLost(self, reason=None):
        log.debug("Protocol lost connection")

    def lineReceived(self, line):
        log.info('Server received: {}'.format(line.strip().decode('utf-8', 'replace')))


class ZombieFactory(Factory):

    def __init__(self):
        pass

    def buildProtocol(self, addr):
        log.info('Remote addr: {}'.format(addr))
        return ZombieProtocol()


def server_process():
    from twisted.internet import reactor
    log.debug('Twisted listening on port {}'.format(settings.DEFAULT_PORT))
    reactor.listenTCP(settings.DEFAULT_PORT, ZombieFactory())
    reactor.run()
