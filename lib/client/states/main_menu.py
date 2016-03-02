from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
import os
from collections import OrderedDict
from .state import BaseState
from ...settings import DATA_DIR, GAME_TITLE
from .base_menu import render_menu_bg

#create a menu object that will accept arrow up and enter to perform actions

class State(BaseState):

    def __init__(self, game):
        super(State, self).__init__(game)
        self.options = [
            ('Host / Single Player', self.doSingleplayer),
            ('Join Server', self.doJoinServer),
            ('Quit', self.doQuit),
        ]
        self.current_option = 0
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
        self.game.gotoState('join_game')

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.doQuit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.doQuit()
                    return

                elif event.key == pygame.K_DOWN:
                    self.current_option += 1
                    if self.current_option >= len(self.options):
                        self.current_option = 0
                elif event.key == pygame.K_UP:
                    self.current_option -= 1
                    if self.current_option < 0:
                        self.current_option = len(self.options)-1
                elif event.key == pygame.K_RETURN:
                    self.currentOptionExecute()
                    return

    def render(self):
        render_menu_bg(self.game.screen)
        posx = 50
        posy = 100
        for i, (name, func) in enumerate(self.options):
            color = (255,255,255)
            if i == self.current_option:
                color = (0,255,0)
            self.game.screen.blit(self.font.render(name, True, color), (posx, posy))
            posy += 50
