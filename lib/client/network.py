from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver

class ZombieClientProtocol(LineReceiver):
    def __init__(self, game):
        self.game = game

    def connectionMade(self):
        self.game.bindToClient(self.sendUserInput)

    def sendUserInput(self, data):
        '''TODO: discrete list of commands'''
        self.sendLine(data)
        

class ZombieClientFactory(protocol.ClientFactory):
    def __init__(self, game):
        self.game = game

    def buildProtocol(self, addr):
        p = ZombieClientProtocol(self.game)
        p.factory = self
        return p

def run_client():
    from twisted.internet import reactor
    factory = ZombieClientFactory()
    # super todo
    
if __name__ == '__main__':
    run_client()
