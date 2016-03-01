from __future__ import absolute_import, division, print_function, unicode_literals

from .base import Entity, Vec, Bbox, move_bbox

class Ball(Entity):

    hWidth = 5.0
    height = 10.0

    def __init__(self, x, y, vx, vy):
        super(Ball, self).__init__()
        self.bbox = Bbox(x, y, self.hWidth, self.height)
        self.velocity = Vec(vx, vy)

    def tick(self):
        self.move()

    def move(self):
        self.bbox = move_bbox(self.bbox, self.velocity)

    def state_repr(self):
        return dict(
            x=self.bbox.x,
            y=self.bbox.y,
            vx=self.velocity.x,
            vy=self.velocity.y
        )
    
