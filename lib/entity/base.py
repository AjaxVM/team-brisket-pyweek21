from __future__ import absolute_import, division, print_function, unicode_literals

import json
import pygame

from collections import namedtuple
from itertools import count

ENTITY_ID_SEQ = count()

Vec = namedtuple('Vec', ['x', 'y'])

class Entity(object):

    '''
    The base entity logic that all entities should be derived from
    alive = alive or dead boolean
    bbox = the hit box of the entity
    velocity = well you know...
    state = string state of entity (examples idle, walking, running)
    resource = path to image for entity
    is_enviornment = boolean is this entity a wall or floor or is it a thing that moves
    '''
    def __init__(
        self,
        alive=False,
        rect=pygame.Rect(0,0,0,0),
        velocity=Vec(0, 0),
        state='',
        resource='',
        is_environment=False
    ):
        self.alive = alive
        self.rect = rect
        self.velocity = velocity
        self.state = state
        self.resource = resource
        self.is_environment=is_environment
        self.__hash = next(ENTITY_ID_SEQ)

    def __repr__(self):
        return self.state

    def __hash__(self):
        return self.__hash

    def set_next_state(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_next_state(self):
        raise NotImplementedError('Implement Me')

    def get_fail_state(self):
        raise NotImplementedError('Implement Me')

    def state_repr(self):
        raise NotImplementedError('Implement Me')


# Also may not be used because moving entities to classes
# class GraphicalEntity(object):

#     def __init__(self, resource):
#         self.resource = resource

#     def __repr__(self):
#         return "{}:{}".format(self.__class__.__name__, self.resource)

