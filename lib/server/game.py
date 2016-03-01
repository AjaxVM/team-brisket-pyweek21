from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import random
import json
from .level_loader import LevelLoader
from twisted.application import service
from twisted.internet import reactor
from ..entity.ball import Ball


log = logging.getLogger(__name__)


class GameServer(service.Service):

    def __init__(self, router):
        self.router = router
        self.is_running = True
        self.level = LevelLoader('level1')
        
        self.entities = [
            Ball(
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

        entity_states = {}

        for entity in self.entities:
            entity.tick()
            entity_states[hash(entity)] = entity.state_repr()
            
        self.router.broadcast(entity_states)


        if self.is_running:
            reactor.callLater(1.0 / 30, self.tick)
