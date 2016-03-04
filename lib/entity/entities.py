from __future__ import absolute_import, division, print_function, unicode_literals

import os
from .. import settings
from .base import Entity as BaseEntity, Vec
from ..shared import constants
import pygame

class ZombieEntity(BaseEntity):

    def __init__(self):
        alive = True
        rect = pygame.Rect(0,0,0,0)

        velocity = Vec(0, 0)
        resource = 'zombie'
        is_enviornment = False
        super(ZombieEntity, self).__init__(alive,  rect, velocity, resource, is_enviornment)


class PlayerEntity(BaseEntity):

    def __init__(self, slot):
        alive=True
        rect = pygame.Rect(0,0,0,0)
        velocity=Vec(0, 0)
        resource = 'player'
        is_enviornment=False
        self.slot = slot
        super(PlayerEntity, self).__init__(alive, rect, velocity, resource, is_enviornment)

    def get_position_from_player_actions(self, actions):
        transition_rect = self.rect.copy()
        if constants.PLAYER_MOVE_RIGHT:
            transition_rect.move_ip(1,0)
        if constants.PLAYER_MOVE_LEFT:
            transition_rect.move_ip(-1,0)
        if constants.PLAYER_MOVE_JUMP:
            transition_rect.move_up(0,5)
        return dict(
            rect=transition_rect
        )

    def state_repr(self):
        return dict(
            x = self.rect.centerx,
            y = self.rect.bottom
        )
            


class WallEntity(BaseEntity):

    def __init__(self):
        alive=False,
        rect = pygame.Rect(0,0,0,0)
        velocity=Vec(0, 0),
        resource='wall',
        is_enviornment=True
        super(WallEntity, self).__init__(alive, rect, velocity, resource, is_enviornment)

