from __future__ import absolute_import, division, print_function, unicode_literals
import logging
from multiprocessing import Process
import pygame
from . import settings
from .client.network import ZombieClientFactory
from .server.network import server_process
from twisted.internet import reactor

log = logging.getLogger(__name__)


def run_game():
    log.info('Starting server')
    server = Process(target=server_process)
    server.start()
    try:
        log.info('Starting pygame')
        factory = ZombieClientFactory()
        reactor.connectTCP('localhost', 10543, factory)
        reactor.run()

    finally:
        server.terminate()  # not great longterm

def run_server():
    server_process()
