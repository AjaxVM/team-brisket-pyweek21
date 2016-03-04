from __future__ import absolute_import, division, print_function, unicode_literals

from .base import Entity as BaseEntity, Vec
import pygame

class Entity(BaseEntity):

    radius = 5

    def __init__(self, x, y, vx, vy):
        super(Entity, self).__init__()
        self.rect = pygame.Rect(x,y,self.radius*2, self.radius*2)
        self.velocity = Vec(vx, vy)

    def get_next_state(self):
        return dict(
            rect = self.rect.move(*self.velocity)
        )

    def get_fail_state(self):
        return dict(
            velocity=Vec(-self.velocity.x, -self.velocity.y)
        )

    def state_repr(self):
        return dict(
            x=self.rect.centerx,
            y=self.rect.bottom,
            vx=self.velocity.x,
            vy=self.velocity.y
        )
    
