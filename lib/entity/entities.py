from __future__ import absolute_import, division, print_function, unicode_literals

from .base import Entity as BaseEntity, Bbox, Vec

class ZombieEntity(BaseEntity):

    def __init__(
        self,
        alive=True,
        bbox=Bbox(0, 0, 0, 0),
        velocity=Vec(0, 0),
        state='idle',
        resource='path/to/image.png',
        is_enviornment=False
    ):
        super(ZombieEntity, self).__init__(alive, bbox, velocity, state, resource, is_enviornment)


class PlayerEntity(BaseEntity):

    def __init__(
        self,
        alive=True,
        bbox=Bbox(0, 0, 0, 0),
        velocity=Vec(0, 0),
        state='idle',
        resource='path/to/image.png',
        is_enviornment=False
    ):
        super(PlayerEntity, self).__init__(alive, bbox, velocity, state, resource, is_enviornment)


class WallEntity(BaseEntity):

    def __init__(
        self,
        alive=True,
        bbox=Bbox(0, 0, 0, 0),
        velocity=Vec(0, 0),
        state='idle',
        resource='path/to/image.png',
        is_enviornment=True
    ):
        super(WallEntity, self).__init__(alive, bbox, velocity, state, resource, is_enviornment)

