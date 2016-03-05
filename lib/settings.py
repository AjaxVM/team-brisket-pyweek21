from __future__ import absolute_import, division, print_function, unicode_literals
import logging.config
import os
from pygame.locals import * #this is potentially a little cluttery but allows us to define constants for controls
from .shared import constants

CLIENT_ENTITY_PREFIX = 'client_'

GAME_TITLE = "Zombie Brisket"
WINDOW_SIZE = (640, 480)
GAME_SIZE = (320,240) #the size we have that is scaled up to window size
FPS = 30
NETWORK_FPS = 10 #how many times a second we send stuff to server
DEFAULT_PORT = 10543
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

NUMBER_OF_PLAYERS = 2

CONTROLS = {
    K_SPACE: constants.PLAYER_MOVE_JUMP
}

HELD_CONTROLS = {
    K_LEFT: constants.PLAYER_MOVE_LEFT,
    K_RIGHT: constants.PLAYER_MOVE_RIGHT,
}

LOGGING = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)-6s %(name)s: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': logging.DEBUG,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': logging.DEBUG,
        },
    },
}

logging.config.dictConfig(LOGGING)
