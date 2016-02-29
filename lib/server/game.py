from __future__ import absolute_import, division, print_function, unicode_literals
from .level_loader import LevelLoader
from twisted.application import service

class GameServer(service.Service):

    def __init__(self):
        self.level = LevelLoader('level1')
