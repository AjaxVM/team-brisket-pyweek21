from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
import os
from .state import BaseState
from ...settings import DATA_DIR, DEFAULT_PORT
from .base_menu import render_menu_bg, CRAP_LOADER, outlined_text
from ...sound.music import set_track


#create a menu object that will accept arrow up and enter to perform actions

class State(BaseState):

    def __init__(self, game):
        super(State, self).__init__(game)
        self.ip_entry = IPEntry(50, 150)
        set_track('COD.mid')

    def doJoinServer(self):
        self.game.game_client.connect(self.ip_entry.text)
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
                elif event.key == pygame.K_RETURN:
                    self.doJoinServer()
                    return
                else:
                    self.ip_entry.handleKey(event.key)

    def render(self):
        render_menu_bg(self.game.screen)
        outlined_text(self.game.screen, CRAP_LOADER['menu_font'], "The server's IP address:", (255, 255, 255), 50, 100)
        outlined_text(self.game.screen, CRAP_LOADER['menu_font'], "* Your friend should open port {}".format(DEFAULT_PORT), (255, 255, 255), 50, 200)
        self.ip_entry.render(self.game.screen)


class IPEntry(object):
    """I can't believe it's a handcoded text field!"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.text = ''
        self.cursor = '*'
        self.width = 150
        self.height = 30
        self.max_len = 16

        # Create a bg that will hold the text
        reffont = CRAP_LOADER['menu_font']
        reftext = reffont.render('M' * self.max_len, True, (0, 0, 0))
        self.width, self.height = reftext.get_size()
        self.bg = pygame.Surface((self.width, self.height))
        self.bg.set_alpha(128)
        self.bg.fill((0, 0, 0))

    def handleKey(self, key):
        # TODO handling for holding down keys -- this has to be done app-wide
        if ord('0') <= key <= ord('9') or key == ord('.'):
            self.text += chr(key)
            self.text = self.text[:self.max_len]
        elif key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]

    def render(self, screen):
        text = CRAP_LOADER['menu_font'].render(self.text, True, (244, 100, 70))
        text_w, text_h = text.get_size()
        text_x, text_y = self.x + 4, self.y + self.height - text_h
        screen.blit(self.bg, (self.x, self.y))
        screen.blit(text, (text_x, text_y))
