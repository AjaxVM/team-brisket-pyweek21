from __future__ import absolute_import, division, print_function, unicode_literals

import os
from .. import settings
from .base import Entity as BaseEntity, Vec
from ..shared import constants
import pygame
import random

class ZombieEntity(BaseEntity):

    def __init__(self, x=0, y=0):
        alive = True
        rect = pygame.Rect(x, y, 18, 18)
        velocity = Vec(0, 0)
        resource = 'plant2'
        is_environment = False
        super(ZombieEntity, self).__init__(alive,  rect, velocity, '', resource, is_environment)
        self.speed = 4
        self.pause = 0

    def state_repr(self):
        return dict(
            x = self.rect.centerx,
            y = self.rect.bottom,
            c = self.__class__.__name__
        )

    def get_next_state(self, game):
        if self.pause:
            self.pause -= 1
            return {'rect': self.rect}
        if random.randint(0, 60) == 0 and game.on_surface(self):
            self.velocity = Vec(self.velocity.x, self.velocity.y - 11)
        elif random.randint(0, 100) == 1:
            self.pause = random.randint(20, 50)
        return {
            'rect': self.rect.move(self.speed, 0),
        }


class PlayerEntity(BaseEntity):

    def __init__(self, slot, x=0, y=0, width=18, height=18):
        alive=True
        rect = pygame.Rect(x, y, width, height)
        velocity=Vec(0, 0)
        resource = 'plant2'
        is_environment=False
        self.slot = slot
        super(PlayerEntity, self).__init__(alive, rect, velocity, '', resource, is_environment)

    def get_position_from_player_actions(self, actions, game):
        transition_rect = self.rect.copy()
        if constants.PLAYER_MOVE_RIGHT in actions:
            transition_rect.move_ip(3,0)
        if constants.PLAYER_MOVE_LEFT in actions:
            transition_rect.move_ip(-3,0)
        if constants.PLAYER_MOVE_JUMP in actions and game.on_surface(self):
            self.velocity = Vec(self.velocity.x, self.velocity.y - 11)
        return {'rect': transition_rect}

    def state_repr(self):
        return dict(
            slot = self.slot,
            x = self.rect.centerx,
            y = self.rect.bottom,
            c = self.__class__.__name__
        )


class WallEntity(BaseEntity):

    def __init__(self, x=0, y=0, resource='red_rock', width=24, height=24):
        alive=False
        rect = pygame.Rect(x, y, width, height)
        velocity=Vec(0, 0)
        resource=resource
        is_environment=True
        super(WallEntity, self).__init__(alive, rect, velocity, '', resource, is_environment)

    def state_repr(self):
        return dict(
            resource = self.resource,
            x = self.rect.centerx,
            y = self.rect.bottom,
            width = self.rect.width,
            height = self.rect.height,
            c = self.__class__.__name__
        )


class DoorEntitiyTop(BaseEntity):

    def __init__(self, x=0, y=0, resource='exit_door_top_left_1', width=24, height=24):
        alive=False
        rect = pygame.Rect(x, y, width, height)
        velocity=Vec(0, 0)
        resource=resource
        is_environment=True
        super(DoorEntitiyTop, self).__init__(alive, rect, velocity, '', resource, is_environment)

    def state_repr(self):
        return dict(
            resource = self.resource,
            x = self.rect.centerx,
            y = self.rect.bottom,
            width = self.rect.width,
            height = self.rect.height,
            c = self.__class__.__name__
        )


class DoorEntitiyBottom(BaseEntity):

    def __init__(self, x=0, y=0, resource='exit_door_top_left_2', width=24, height=24):
        alive=False
        rect = pygame.Rect(x, y, width, height)
        velocity=Vec(0, 0)
        resource=resource
        is_environment=True
        super(DoorEntitiyBottom, self).__init__(alive, rect, velocity, '', resource, is_environment)

    def state_repr(self):
        return dict(
            resource = self.resource,
            x = self.rect.centerx,
            y = self.rect.bottom,
            width = self.rect.width,
            height = self.rect.height,
            c = self.__class__.__name__
        )

