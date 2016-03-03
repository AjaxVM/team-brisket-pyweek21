from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
from .state import BaseState
from ... import settings
from ...shared import constants
from ...sound.music import set_track
from ...world.world import World
from ...entity.ball import Ball
from ...entity.base import Bbox

import logging
log = logging.getLogger(__name__)

#state for playing the game

class State(BaseState):

    def __init__(self, game):
        super(State, self).__init__(game)

        self.movement_actions = [
            constants.PLAYER_MOVE_RIGHT,
            constants.PLAYER_MOVE_LEFT,
            constants.PLAYER_MOVE_JUMP
        ]

        set_track('bjorn__lynne-_no_survivors_.mid')
        self.world = World()

    def backToMenu(self):
        self.game.game_client.disconnect()
        self.game.gotoState('main_menu')

    def doAction(self, action):
        if action in self.movement_actions:
            self.game.game_client.command(action)

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.forceQuit()
                return
            elif event.type == pygame.KEYDOWN:
                log.info('Got Key Event: '+str(event))
                if event.key == pygame.K_ESCAPE:
                    self.backToMenu()
                    return

                elif event.key in settings.CONTROLS:
                    self.doAction(settings.CONTROLS[event.key])

    def render(self):
        for entity in self.world.entities.itervalues():
            pygame.draw.circle(self.game.screen, (255, 0, 0), (int(entity.bbox.x), int(entity.bbox.y)), 5)

    def objectReceived(self, obj):
        # hardcoded hack for now
        for id, data in obj.iteritems():
            entity = self.world.entities.get(id)
            if entity is None:
                entity = self.world.entities[id] = Ball(0, 0, 0, 0)
            self.world.entities[id].bbox = Bbox(data['x'], data['y'], entity.bbox.hwidth, entity.bbox.height)
