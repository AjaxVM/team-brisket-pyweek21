from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import random
import json
from .level_loader import LevelLoader
from twisted.application import service
from twisted.internet import reactor
from ..entity import entities
from ..entity.base import Vec
from .. import settings
from ..shared import constants
from collections import deque


log = logging.getLogger(__name__)


class GameServer(service.Service):

    def __init__(self, router):
        self.router = router
        self.is_running = False
        self.action_buffer = {
            i: deque() for i in xrange(1, settings.NUMBER_OF_PLAYERS + 1)
        }
        self.fps = 1.0 / settings.FPS
        self.entities = []
        self.player_entity_hashes = {}

        #TODO: should loadLevel reset entities so we can load more levels, or should this not happen at init?
        self.loadLevel('level2')

    def loadLevel(self, name):
        level = LevelLoader(name)

        for ent in level.grid_elements:
            # TODO: handle the proper resource from ent[0]
            posx,posy = ent[1]
            posy = settings.GAME_SIZE[1]-posy
            print(ent[0])
            self.entities.append(
                ent[0](posx, posy)
            )

    def playerJoin(self, slot):
        self.start()
        player_entity = entities.PlayerEntity(slot=slot)
        self.player_entity_hashes[hash(player_entity)] = slot
        self.entities.append(player_entity)

    def playerLeave(self, slot):
        if self.router.empty():
            self.stop()

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.entities = []
            self.player_entity_hashes = {}
            self.loadLevel('level2')
            reactor.callLater(1.0 / 30, self.tick)
            log.debug('Starting server game loop')

    def stop(self):
        self.is_running = False
        log.debug('Stopping server game loop')

    def tick(self):

        failures = {}

        potential_entity_states = {}
        for entity in self.entities:
            key = hash(entity)
            if key in self.player_entity_hashes:
                slot = self.player_entity_hashes[key]
                player_actions = self.action_buffer[slot].popleft() if self.action_buffer[slot] else []
                potential_entity_states[key] = entity.get_position_from_player_actions(player_actions, self)
                # log.debug('slot {} now at {}'.format(slot, potential_entity_states[key]))
            else:
                potential_entity_states[key] = entity.get_next_state()

        for key_a, state_a in potential_entity_states.iteritems():
            for key_b, state_b in potential_entity_states.iteritems():
                if key_a < key_b:
                    if state_a['rect'].colliderect(state_b['rect']):
                        log.debug('collision detected')
                        failures[key_b] = 1

        for entity in self.entities:
            key = hash(entity)
            if key in failures:
                entity.set_next_state(**entity.get_fail_state())
            else:
                entity.set_next_state(**potential_entity_states[key])

        # physics
        for entity in self.entities:
            # gravity
            if not entity.is_environment:  # don't actually like this
                entity.velocity = Vec(entity.velocity.x, min(15, entity.velocity.y + 1))
                physics_state = entity.rect.copy()
                physics_state.move_ip(entity.velocity.x, entity.velocity.y)
                entity.rect = physics_state
                for e2 in self.entities:
                    if e2.is_environment and entity.rect.colliderect(e2.rect):
                        if e2.rect.y > entity.rect.y:
                            physics_state.move_ip(0, -(physics_state.y + physics_state.height - e2.rect.y))
                        else:
                            physics_state.move_ip(0, -(physics_state.midtop[1] - e2.rect.midbottom[1]))
                        entity.velocity = Vec(entity.velocity.x, 0)

        self.router.broadcast({hash(entity): entity.state_repr() for entity in self.entities})

        if self.is_running:
            reactor.callLater(1.0 / 30, self.tick)

    def push_actions(self, slot, actions):
        log.debug('received {} from client'.format(json.dumps(actions)))
        self.action_buffer[slot].extend(actions)

    def on_surface(self, entity):
        rect = entity.rect.move(0, 1)
        for e2 in self.entities:
            if e2.is_environment and rect.colliderect(e2.rect):
                return True
        return False
