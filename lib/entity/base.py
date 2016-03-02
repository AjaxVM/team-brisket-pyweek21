from __future__ import absolute_import, division, print_function, unicode_literals

import json

from collections import namedtuple
from itertools import count

ENTITY_ID_SEQ = count()

Vec = namedtuple('Vec', ['x', 'y'])

# Point is center bottom. hwidth is half width and height is full height
Bbox = namedtuple('Bbox', ['x', 'y', 'hwidth', 'height'])


def process_json(json_to_parse):
    new_bbox = Bbox(
        json_to_parse.get('hitBox_x'),
        json_to_parse.get('hitBox_y'),
        json_to_parse.get('hitBox_hWidth'),
        json_to_parse.get('hitBox_height')
    )
    new_vec = Vec(
        json_to_parse.get('vex_x'),
        json_to_parse.get('vex_y')
    )

    entity = Entity(
        json_to_parse.get('alive'),
        new_bbox,
        new_vec,
        json_to_parse.get('state')
    )

    graphic = GraphicalEntity(json_to_parse.get('resource'))

    return [entity, graphic]


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

    def __init__(self, alive=False, bbox=Bbox(0, 0, 0, 0), velocity=Vec(0, 0), state=''):
        self.alive = alive
        self.bbox = bbox
        self.velocity = velocity
        self.state = state
        self.__hash = next(ENTITY_ID_SEQ)

    def __repr__(self):
        return "<{0} x{1.x} y{1.y} hw{1.hwidth} h{1.height} vx{3.x} vy{3.y}>".format(
            self.__class__.__name__,
            self.bbox,
            self.velocity
        )

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

class GraphicalEntity(object):

    def __init__(self, resource):
        self.resource = resource

    def __repr__(self):
        return "{}:{}".format(self.__class__.__name__, self.resource)

