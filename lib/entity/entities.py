from __future__ import absolute_import, division, print_function, unicode_literals

import os
from .. import settings
from .base import Entity as BaseEntity, Bbox, Vec
from ..shared import constants

class ZombieEntity(BaseEntity):

    def __init__(self):
        alive=True
        bbox=Bbox(0, 0, 0, 0)
        velocity=Vec(0, 0)
        resource = os.path.join(settings.DATA_DIR, 'assets', 'entities', 'zombie.png')
        is_enviornment=False
        super(ZombieEntity, self).__init__(alive, bbox, velocity, resource, is_enviornment)


class PlayerEntity(BaseEntity):

    def __init__(self, slot):
        alive=True
        bbox=Bbox(0, 0, 0, 0)
        velocity=Vec(0, 0)
        resource = os.path.join(settings.DATA_DIR, 'assets', 'entities', 'testplayer.png')
        is_enviornment=False
        self.slot = slot
        super(PlayerEntity, self).__init__(alive, bbox, velocity, resource, is_enviornment)

    def get_position_from_player_actions(self, actions):
        transition_bbox = self.bbox
        if constants.PLAYER_MOVE_RIGHT in actions:
            transition_bbox = Bbox(transition_bbox.x + 1, transition_bbox.y, transition_bbox.hwidth, transition_bbox.height)
        if constants.PLAYER_MOVE_LEFT in actions:
            transition_bbox = Bbox(transition_bbox.x - 1, transition_bbox.y, transition_bbox.hwidth, transition_bbox.height)
        if constants.PLAYER_MOVE_JUMP in actions:
            transition_bbox = Bbox(transition_bbox.x, transition_bbox.y - 5, transition_bbox.hwidth, transition_bbox.height)
        return dict(
            bbox=transition_bbox
        )

    def state_repr(self):
        return dict(
            x=self.bbox.x,
            y=self.bbox.y
        )
            


class WallEntity(BaseEntity):

    def __init__(self):
        alive=False,
        bbox=Bbox(0, 0, 0, 0),
        velocity=Vec(0, 0),
        resource='path/to/image.png',
        is_enviornment=True
        super(WallEntity, self).__init__(alive, bbox, velocity, resource, is_enviornment)

