from __future__ import absolute_import, division, print_function, unicode_literals
import logging
from multiprocessing import Process
import pygame
from . import settings
from .client.network import ZombieClientFactory
from twisted.internet import reactor
from .server.network import server_process

log = logging.getLogger(__name__)


def run_game():
    log.info('Starting game factory')
    factory = ZombieClientFactory()
    reactor.run()

def run_server():
    server_process()
