from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
from .state import BaseState

#create a menu object that will accept arrow up and enter to perform actions

class State(BaseState):

    def __init__(self, game):
        super(State, self).__init__(game)

        self.options = {
            'Singleplayer [Hosts server and plays]': self.doSingleplayer,
            'Join Server [expects a server is running @ localhost]': self.doJoinServer,
            'Quit': self.doQuit
        }

        self.option_keys = [
            'Singleplayer [Hosts server and plays]',
            'Join Server [expects a server is running @ localhost]',
            'Quit'
        ]

        self.current_option = 0

        self.font = pygame.font.Font(None, 26)

    def currentOption(self):
        return self.option_keys[self.current_option]

    def currentOptionExecute(self):
        self.options[self.currentOption()]()

    def doQuit(self):
        self.game.forceQuit()

    def doSingleplayer(self):
        self.game.game_client.startLocalServer()
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
                    self.doQuit()
                    return

                elif event.key == pygame.K_DOWN:
                    self.current_option += 1
                    if self.current_option >= len(self.option_keys):
                        self.current_option = 0
                elif event.key == pygame.K_UP:
                    self.current_option -= 1
                    if self.current_option < 0:
                        self.current_option = len(self.option_keys)-1
                elif event.key == pygame.K_RETURN:
                    self.currentOptionExecute()
                    return

    def render(self):
        posx = 50
        posy = 100
        for i in self.option_keys:
            color = (255,255,255)
            if i == self.currentOption():
                color = (0,255,0)
            self.game.screen.blit(self.font.render(i, True, color), (posx, posy))
            posy += 50


