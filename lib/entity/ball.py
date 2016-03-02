from __future__ import absolute_import, division, print_function, unicode_literals

from .base import Entity as BaseEntity, Vec, Bbox, move_bbox

class Entity(BaseEntity):

    hWidth = 5.0
    height = 10.0

    def __init__(self, x, y, vx, vy):
        super(Entity, self).__init__()
        self.bbox = Bbox(x, y, self.hWidth, self.height)
        self.velocity = Vec(vx, vy)

    def get_next_state(self):
        return dict(
            bbox=move_bbox(self.bbox, self.velocity)
        )

    def get_fail_state(self):
        return dict(
            velocity=Vec(-self.velocity.x, -self.velocity.y)
        )

    def state_repr(self):
        return dict(
            x=self.bbox.x,
            y=self.bbox.y,
            vx=self.velocity.x,
            vy=self.velocity.y
        )
    
