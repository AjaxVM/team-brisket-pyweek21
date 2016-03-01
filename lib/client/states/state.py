from __future__ import absolute_import, division, print_function, unicode_literals
import pygame

# this is the core state object

class BaseState(object):
    def __init__(self, game):
        self.game = game

    def leave(self):
        #buh bye - cleanup stuff
        pass

    def render(self):
        #do render stuff
        pass

    def handleEvents(self):
        #do event stuff
        #basic setup that allows quitting

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.forceQuit()
                return
            elif event.type == pygame.KEYDOWN:
                log.info('Got Key Event: '+str(event))
                if event.key == pygame.K_ESCAPE:
                    self.game.forceQuit()
                    return
