from __future__ import absolute_import, division, print_function, unicode_literals
from .level_loader import LevelLoader


class GameServer(object):

    def __init__(self):
        self.level = LevelLoader('level1')
