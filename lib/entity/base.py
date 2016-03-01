from __future__ import absolute_import, division, print_function, unicode_literals
from collections import namedtuple
from itertools import count

ENTITY_ID_SEQ = count()

Vec = namedtuple('Vec', ['x', 'y'])

# Point is center bottom. hwidth is half width and height is full height
Bbox = namedtuple('Bbox', ['x', 'y', 'hwidth', 'height'])


def bbox_collides(a, b):
    return not (
        a.x + a.hwidth < b.x - b.hwidth
        or b.x + b.hwidth < a.x - a.hwidth
        or a.y + a.height < b.y
        or b.y + b.height < a.y
    )


def move_bbox(bbox, vec):
    return Bbox(bbox.x + vec.x, bbox.y + vec.y, bbox.hwidth, bbox.height)


class Entity(object):

    bbox = Bbox(0, 0, 0, 0)
    velocity = Vec(0, 0)
    alive = False

    def __init__(self):
        self.__hash = next(ENTITY_ID_SEQ)

    def __repr__(self):
        return "<{0} x{1.x} y{1.y} hw{1.hwidth} h{1.height} vx{3.x} vy{3.y}>".format(self.__class__.__name__, self.bbox, self.velocity)

    def __hash__(self):
        return self.__hash

    def tick(self):
        raise NotImplementedError('Implement Me')

    def state_repr(self):
        raise NotImplementedError('Implement Me')

