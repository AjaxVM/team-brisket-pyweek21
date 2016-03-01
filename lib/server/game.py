from __future__ import absolute_import, division, print_function, unicode_literals
import logging
from .level_loader import LevelLoader
from twisted.application import service
from twisted.internet import reactor


log = logging.getLogger(__name__)


class GameServer(service.Service):

    def __init__(self, router):
        self.router = router
        self.is_running = True
        self.level = LevelLoader('level1')

        self.ball_y = 400.0
        self.ball_v = 0.0
        self.gravity = -0.1

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

        new_ball_y = self.ball_y + self.ball_v
        self.ball_v += self.gravity
        if new_ball_y <= 0:
            self.ball_y = 0.0
            self.ball_v = -self.ball_v * 0.9
        else:
            self.ball_y = new_ball_y
        self.router.broadcast({'ball_y': int(self.ball_y)})


        if self.is_running:
            reactor.callLater(1.0 / 30, self.tick)
