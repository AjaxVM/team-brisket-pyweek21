from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import random
import json
from .level_loader import LevelLoader
from twisted.application import service
from twisted.internet import reactor
from ..entity import entities
# from ..entity.base import bbox_collides
from .. import settings
from ..shared import constants
from collections import deque


log = logging.getLogger(__name__)


class GameServer(service.Service):

    def __init__(self, router):
        self.router = router
        self.is_running = True
        self.level = LevelLoader('level1')

        self.action_buffer = {
            i: deque() for i in xrange(1, settings.NUMBER_OF_PLAYERS + 1)
        }

        self.fps = 1.0 / settings.FPS
        
        self.entities = []
        self.player_entity_hashes = {}

    def playerJoin(self, slot):
        player_entity = entities.PlayerEntity(slot=slot)
        self.player_entity_hashes[hash(player_entity)] = slot
        self.entities.append(player_entity)
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

        potential_entity_states = {}
        for entity in self.entities:
            key = hash(entity)
            if key in self.player_entity_hashes:
                slot = self.player_entity_hashes[key]
                player_actions = self.action_buffer[slot].popleft() if self.action_buffer[slot] else []
                potential_entity_states[key] = entity.get_position_from_player_actions(player_actions)
                log.debug('slot {} now at {}'.format(slot, potential_entity_states[key]))
            else:
                potential_entity_states[key] = entity.get_next_state()

        for key_a, entity_a in potential_entity_states.iteritems():
            for key_b, entity_b in potential_entity_states.iteritems():
                if key_a < key_b:
                    if entity_a.rect.colliderect(entity_b.rect):
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

    def push_actions(self, slot, actions):
        log.debug('received {} from client'.format(json.dumps(actions)))
        self.action_buffer[slot].extend(actions)
        
