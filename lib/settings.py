from __future__ import absolute_import, division, print_function, unicode_literals
import logging.config
import os


GAME_TITLE = "Zombie Brisket"
WINDOW_SIZE = (600, 600)
FPS = 60
DEFAULT_PORT = 10543
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

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
