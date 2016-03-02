from __future__ import absolute_import, division, print_function, unicode_literals

from .base import Entity as BaseEntity, Bbox

class Entity(BaseEntity):

    hWidth = 20.0
    height = 20.0

    def __init__(self, x, y, vx, vy):
        super(Entity, self).__init__()
        self.bbox = Bbox(x, y, self.hWidth, self.height)

    def get_next_state(self):
        return dict()

    def get_fail_state(self):
        return dict()

    def state_repr(self):
        return dict(
            x=self.bbox.x,
            y=self.bbox.y,
        )
