from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
import os, json
import logging
from .. import settings
from ..shared import constants
from ..entity import entities

log = logging.getLogger(__name__)

#CONSTANTS
# LEVEL_GRID_WIDTH = 32
# LEVEL_GRID_HEIGHT = 32

LEVEL_GRID_COLOR_MAP = {
    '255,255,255': 'nothing', #this should never show up
    '0,0,0':       entities.WallEntity, #bottom of level
    '255,0,0':     entities.WallEntity, #instant death
    '0,255,0':     entities.WallEntity, #yay
    '0,0,255':     entities.WallEntity, #platform, but slidy...
    '100,100,100': entities.DoorEntitiyTop, #platforms but look cooler
    '200,200,200': entities.DoorEntitiyBottom, #get here to pass level
}

class LevelLoader(object):
    def __init__(self, level):

        self.level = level

        self.config_path = os.path.join(settings.DATA_DIR, 'levels', level+'.json')
        self.image_path = os.path.join(settings.DATA_DIR, 'levels', level+'.png')

        self.parseConfig()
        self.parseImage()

        log.info('Loaded level: %s'%self.level_name)

    def parseConfig(self):
        config = json.loads(open(self.config_path, 'rb').read())
        self.level_name = config["levelName"]

    def parseImage(self):
        self.image = pygame.image.load(self.image_path)
        self.grid_size = (0,0)

        #list of elements which are (tile_type, pos(x,y))
        #FYI: these are a little odd in that y 0 is at bottom of screen, but in pygame y 0 is top
        #also, these represent the coordinates of the center of the tiles
        self.grid_elements = []
        self.grid_size = self.image.get_size()
        self.level_bounds = (0, 0, self.grid_size[0]*constants.LEVEL_GRID_WIDTH, self.grid_size[1]*constants.LEVEL_GRID_HEIGHT)

        for x in xrange(self.grid_size[0]):
            for y in xrange(self.grid_size[1]):
                pos = (x,y)
                color = "%s,%s,%s"%(self.image.get_at(pos)[:3])
                if color == '255,255,255':
                    continue
                self.grid_elements.append((LEVEL_GRID_COLOR_MAP[color],
                                           (int((pos[0])*constants.LEVEL_GRID_WIDTH),
                                            int((self.grid_size[1]-pos[1])*constants.LEVEL_GRID_HEIGHT)
                                           )))

        # log.info(self.grid_elements)


