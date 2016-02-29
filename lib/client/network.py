from twisted.internet import protocol
from ..shared.protocol import JsonReceiver
from ..shared import constants
import pygame

class ZombieClientProtocol(JsonReceiver):
    # todo: move all potential client and server 'directives' (commands) to constants
    key_mapping = {
        constants.STATE_ACTION: {
            pygame.K_LEFT: 'left',
            pygame.K_RIGHT: 'right',
            pygame.K_z: 'jump',
            pygame.K_ESCAPE: 'quit',
        },
        constants.STATE_WAITING: {
            pygame.K_ESCAPE: 'quit',
        },
    }

    def __init__(self, game):
        self.game = game

    def connectionMade(self):
        self.game.bindToClient(self.sendUserInput)

    def sendUserInput(self, data):
        if self.game.state == constants.STATE_INTRO:
            self.sendCommand('salutation', name=data)
        else:
            if data in self.key_mapping[self.game.state]:
                self.sendCommand(self.key_mapping[self.game.state][data])

    def sendCommand(self, command, **kwargs):
        self.sendObject(command=command, params=kwargs)
        

    
        

class ZombieClientFactory(protocol.ClientFactory):
    def __init__(self, game):
        self.game = game

    def buildProtocol(self, addr):
        p = ZombieClientProtocol(self.game)
        p.factory = self
        return p
    
