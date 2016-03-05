from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
from .state import BaseState
from ... import settings
from ...shared import constants
from ...sound.music import set_track
from ...entity import entities

import logging
log = logging.getLogger(__name__)

from ...entity.entities import PlayerEntity

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

        self.view_screen = pygame.Surface(settings.GAME_SIZE)
        self.viewport = self.view_screen.get_rect()
        self.players = []

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
        held_keys = pygame.key.get_pressed()
        for key, action in settings.HELD_CONTROLS.iteritems():
            if held_keys[key]:
                self.doAction(action)

    def move_viewport(self):
        #set viewportx to center between all players, and bottom to player bottom+one tile size
        if self.players:
            x = int(sum(player.rect.centerx for player in self.players) / len(self.players))
            y = int(sum(player.rect.bottom for player in self.players) / len(self.players)) + constants.LEVEL_GRID_HEIGHT * 2
            self.viewport.midbottom = (x,y)

            if self.viewport.left < 0:
                self.viewport.left = 0
            # TODO: better/more robust way to handle finding the right bounds
            m = max(entity.rect.right for entity_id, entity in self.entities.iteritems() if not entity in self.players)
            if self.viewport.right > m:
                self.viewport.right = m

    def render(self):
        self.view_screen.fill((0,0,0))
        self.move_viewport()
        for entity_id, entity in self.entities.iteritems():
            RESOURCE.blit(self.view_screen,
                          entity.tileset,
                          entity.resource,
                          entity.rect.move((-self.viewport.left, -self.viewport.top)))
        pygame.transform.scale(self.view_screen, settings.WINDOW_SIZE, self.game.screen)

    def objectReceived(self, obj):
        # TODO way to distinguish different things the server sends, right now we're assuming its entity positions
        for entity_id, data in obj.iteritems():
            entity = self.entities.get(entity_id)
            if entity is None:
                klass = getattr(entities, data.pop('c'))
                entity = self.entities[entity_id] = klass(**data)
                if isinstance(entity, entities.PlayerEntity) and not any(hash(player) == entity_id for player in self.players):
                    self.players.append(entity)
            newx = data.get('x', entity.rect.centerx)
            newy = data.get('y', entity.rect.bottom)
            entity.rect.midbottom = (newx, newy)


def draw_tilebox(screen, tileset, base_name, sx, sy, width_tiles, height_tiles):
    """Debug func for drawing a box out of tiles. Probably not using because
    they will be individual entities."""
    _draw_tilebox_row(screen, tileset, base_name, sx, sy, width_tiles, '_top_left', '_top', '_top_right')
    for i in xrange(1, height_tiles - 1):
        _draw_tilebox_row(screen, tileset, base_name, sx, sy + i * 24, width_tiles, '_left', '', '_right')
    _draw_tilebox_row(screen, tileset, base_name, sx, sy + (height_tiles - 1) * 24, width_tiles, '_bot_left', '_bot', '_bot_right')


def _draw_tilebox_row(screen, tileset, base_name, sx, sy, width_tiles, left_name, mid_name, right_name):
    RESOURCE.blit(screen, tileset, base_name + left_name, (sx, sy))
    for i in xrange(1, width_tiles - 1):
        RESOURCE.blit(screen, tileset, base_name + mid_name, (sx + i * 24, sy))
    RESOURCE.blit(screen, tileset, base_name + right_name, (sx + (width_tiles - 1) * 24, sy))
