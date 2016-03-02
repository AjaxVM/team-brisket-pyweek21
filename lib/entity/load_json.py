from __future__ import absolute_import, division, print_function, unicode_literals

import os
import json

from base import Bbox, Vec, Entity, GraphicalEntity


def process_json(path_to_entity_data):
    RESOURCE_BASE_PATH = os.path.join(os.getcwd(), 'data', 'resources')
    ASSETS_BASE_PATH = os.path.join(os.getcwd(), 'data', 'assets')

    entity_data = json.load(open(path_to_entity_data))
    resource_data = json.load(open(os.path.join(RESOURCE_BASE_PATH, entity_data.get('resource'))))

    new_bbox = Bbox(
        entity_data.get('hitBox_x'),
        entity_data.get('hitBox_y'),
        entity_data.get('hitBox_hWidth'),
        entity_data.get('hitBox_height')
    )
    new_vec = Vec(
        entity_data.get('vex_x'),
        entity_data.get('vex_y')
    )

    entity = Entity(
        entity_data.get('alive'),
        entity_data.get('health'),
        new_bbox,
        new_vec,
        entity_data.get('state')
    )

    graphic = GraphicalEntity(os.path.join(ASSETS_BASE_PATH, resource_data.get('resource_path')))

    return [entity, graphic]

