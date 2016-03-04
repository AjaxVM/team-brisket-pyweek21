from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
from .state import BaseState
from ... import settings
from ...shared import constants
from ...sound.music import set_track

import logging
log = logging.getLogger(__name__)

from ...entity.entities import PlayerEntity
from ...entity.base import Bbox

#state for playing the game

from ..resource import Resource
RESOURCE = Resource()


class State(BaseState):

    def __init__(self, game):
        super(State, self).__init__(game)

        self.movement_actions = [
            constants.PLAYER_MOVE_RIGHT,
            constants.PLAYER_MOVE_LEFT,
            constants.PLAYER_MOVE_JUMP
        ]

        self.entities = {}  # for now

        set_track('bjorn__lynne-_no_survivors_.mid')

    def backToMenu(self):
        self.game.game_client.disconnect()
        self.game.gotoState('main_menu')

    def doAction(self, action):
        if action in self.movement_actions:
            self.game.game_client.command('move', action=action)

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
        screen = self.game.screen
        draw_tilebox(screen, 'hostile_planet', 'red_rock', 10, 10, 8, 8)
        for entity_id, entity in self.entities.iteritems():
            RESOURCE.blit(screen, 'hostile_planet', 'plant2', entity.bbox.x, entity.bbox.y + 300)

    def objectReceived(self, obj):
        # TODO way to distinguish different things the server sends, right now we're assuming its entity positions
        for entity_id, data in obj.iteritems():
            entity = self.entities.get(entity_id)
            if entity is None:
                entity = self.entities[entity_id] = PlayerEntity(0)  # note: we are't sending the slot down either?
            newx = data.get('x', entity.bbox.x)
            newy = data.get('y', entity.bbox.y)
            entity.bbox = Bbox(newx, newy, entity.bbox.hwidth, entity.bbox.height)


def draw_tilebox(screen, tileset, base_name, sx, sy, width_tiles, height_tiles):
    """Debug func for drawing a box out of tiles. Probably not using because
    they will be individual entities."""
    _draw_tilebox_row(screen, tileset, base_name, sx, sy, width_tiles, '_top_left', '_top', '_top_right')
    for i in xrange(1, height_tiles - 1):
        _draw_tilebox_row(screen, tileset, base_name, sx, sy + i * 24, width_tiles, '_left', '', '_right')
    _draw_tilebox_row(screen, tileset, base_name, sx, sy + (height_tiles - 1) * 24, width_tiles, '_bot_left', '_bot', '_bot_right')


def _draw_tilebox_row(screen, tileset, base_name, sx, sy, width_tiles, left_name, mid_name, right_name):
    RESOURCE.blit(screen, tileset, base_name + left_name, sx, sy)
    for i in xrange(1, width_tiles - 1):
        RESOURCE.blit(screen, tileset, base_name + mid_name, sx + i * 24, sy)
    RESOURCE.blit(screen, tileset, base_name + right_name, sx + (width_tiles - 1) * 24, sy)
