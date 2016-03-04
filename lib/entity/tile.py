from __future__ import absolute_import, division, print_function, unicode_literals

from .base import Entity as BaseEntity#, Bbox
from ..shared import constants

class Entity(BaseEntity):

    hWidth = 20.0
    height = 20.0

    def __init__(self, x, y, vx, vy):
        super(Entity, self).__init__()
        self.rect = pygame.Rect(x,y,constants.LEVEL_GRID_WIDTH,constants.LEVEL_GRID_HEIGHT)

    def get_next_state(self):
        return dict()

    def get_fail_state(self):
        return dict()

    def state_repr(self):
        return dict(
            x=self.rect.centerx,
            y=self.bbox.bottom
        )
