from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import random
import json
from .level_loader import LevelLoader
from twisted.application import service
from twisted.internet import reactor
from ..entity import ball
from ..entity.base import bbox_collides


log = logging.getLogger(__name__)


class GameServer(service.Service):

    def __init__(self, router):
        self.router = router
        self.is_running = True
        self.level = LevelLoader('level1')
        
        self.entities = [
            ball.Entity(
                random.uniform(0, 640),
                random.uniform(0, 480),
                random.uniform(-5, 5),
                random.uniform(-5, 5)
            )
            for _ in xrange(10)
        ]

    def playerJoin(self, slot):
        self.start()

    def playerLeave(self, slot):
        if self.router.empty():
            self.stop()

    def start(self):
        if not self.running:
            self.is_running = True
            reactor.callLater(1.0 / 30, self.tick)
            log.debug('Starting server game loop')

    def stop(self):
        self.running = False
        log.debug('Stopping server game loop')

    def tick(self):

        failures = {}

        potential_entity_states = {hash(entity): entity.get_next_state() for entity in self.entities}

        for key_a, entity_a in potential_entity_states.iteritems():
            for key_b, entity_b in potential_entity_states.iteritems():
                if key_a < key_b:
                    if bbox_collides(entity_a['bbox'], entity_b['bbox']):
                        log.debug('collision detected')
                        failures[key_b] = 1

        for entity in self.entities:
            key = hash(entity)
            if key in failures:
                entity.set_next_state(**entity.get_fail_state())
            else:
                entity.set_next_state(**potential_entity_states[key])
                                                            
        self.router.broadcast({hash(entity): entity.state_repr() for entity in self.entities})


        if self.is_running:
            reactor.callLater(1.0 / 30, self.tick)
