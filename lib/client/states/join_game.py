from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
import os
from collections import OrderedDict
from .state import BaseState
from ...settings import DATA_DIR, GAME_TITLE

#create a menu object that will accept arrow up and enter to perform actions

class State(BaseState):

    def __init__(self, game):
        super(State, self).__init__(game)
        self.font = pygame.font.Font(os.path.join(DATA_DIR, 'fonts/ShadowsIntoLight.ttf'), 26)

    def currentOptionExecute(self):
        name, func = self.options[self.current_option]
        func()

    def doQuit(self):
        self.game.forceQuit()

    def doSingleplayer(self):
        self.game.game_client.connect()
        self.game.gotoState('play_game')

    def doJoinServer(self):
        self.game.game_client.connect()
        self.game.gotoState('play_game')

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.doQuit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.gotoState('main_menu')
                    return

    def render(self):
        self.game.screen.blit(self.font.render(GAME_TITLE, True, (244, 100, 70)), (10, 10))

