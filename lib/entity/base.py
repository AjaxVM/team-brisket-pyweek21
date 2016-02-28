from __future__ import absolute_import, division, print_function, unicode_literals
from collections import namedtuple


Vec = namedtuple('Vec', ['x', 'y'])
Bbox = namedtuple('Bbox', ['x', 'y', 'x2', 'y2'])


def bbox_collides(a, b):
    return not (
        a.x > b.x2
        or a.y > b.y2
        or a.x2 < b.x
        or a.y2 < b.y
    )


def width_height(bbox):
    return Vec(bbox.x2 - bbox.x, bbox.y2 - bbox.y)


def move_bbox(bbox, vec):
    return Bbox(bbox.x + vec.x, bbox.y + vec.y, bbox.x2 + vec.x, bbox.y2 + vec.y)


class Entity(object):

    def __init__(self):
        self.alive = False
        self.bbox = Bbox(0, 0, 0, 0)
        self.velocity = Vec(0, 0)

    def __repr__(self):
        return "<{0} x{1.x} y{1.y} w{2.x} h{2.y} vx{3.x} vy{3.y}>".format(self.__class__.__name__, self.bbox, width_height(self.bbox), self.velocity)
