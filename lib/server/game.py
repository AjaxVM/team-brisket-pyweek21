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

        # Hardcoded zombies for now
        for i in range(3):
            self.entities.append(entities.ZombieEntity(0, 0))

    def playerJoin(self, slot):
        self.start()
        player_entity = entities.PlayerEntity(slot=slot)
        self.player_entity_hashes[hash(player_entity)] = slot
        self.entities.append(player_entity)
        self.router.broadcast({hash(entity): entity.state_repr() for entity in self.entities})

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
        entity_list = self.entities
        updated = []

        # Apply gravity
        for entity in entity_list:
            entity.velocity = Vec(entity.velocity.x, min(15, entity.velocity.y + 1))

        # Movement and collisions
        for entity in entity_list:
            orig_rect = entity.rect.copy()
            if entity.is_environment:
                # For now environment is immobile
                continue
            if type(entity) is entities.PlayerEntity:
                slot = self.player_entity_hashes[entity]
                player_actions = self.action_buffer[slot].popleft() if self.action_buffer[slot] else []
                new_state = entity.get_position_from_player_actions(player_actions, self)
            else:
                new_state = entity.get_next_state(self)
            new_rect = new_state.get('rect', entity.rect)
            # First collide on the entity's action
            for e2 in entity_list:
                if e2.is_environment and new_rect.colliderect(e2.rect):
                    new_rect = entity.rect
                    break
            entity.rect = new_rect
            # Next collide the physics vector
            new_rect = new_rect.move(entity.velocity.x, entity.velocity.y)
            for e2 in entity_list:
                if e2.is_environment and new_rect.colliderect(e2.rect):
                    # Work backward from new_rect to one that doesn't collide
                    # For now we only have gravity so doing this without the x component as a hack
                    sign = -1 if new_rect.y > entity.rect.y else 1
                    while new_rect.y != entity.rect.y:
                        new_rect.y += sign
                        if not new_rect.colliderect(e2.rect):
                            break
                    else:
                        new_rect = entity.rect
                    entity.velocity = Vec(entity.velocity.x, 0)
            if new_rect != orig_rect:
                updated.append(entity)
            entity.rect = new_rect

        self.router.broadcast({hash(entity): entity.state_repr() for entity in updated})
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


def collide_entities(entities):
    for i1, e1 in enumerate(entities):
        for i2, e2 in enumerate(entities):
            if i2 > i1 and e1.rect.colliderect(e2.rect):
                yield (e1, e2)
