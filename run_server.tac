from twisted.application import internet, service
from lib.server.network import ZombieFactory
from lib.server.game import GameServer
from lib import settings

interface = 'localhost'

top_service = service.MultiService()

game_service = GameServer()
game_service.setServiceParent(top_service)

factory = ZombieFactory(game_service)
tcp_service = internet.TCPServer(settings.DEFAULT_PORT, factory, interface=interface)
tcp_service.setServiceParent(top_service)

application = service.Application("brisket-zombie-server")

top_service.setServiceParent(application)