from __future__ import absolute_import, division, json, print_function, unicode_literals


def process_json(json_to_parse):
    '''
    Takes json from the server or the client and xforms it into a logical entity and a graphical entity
    '''

    # Allows for any number of properties to be defined within the configs
    # which will be pulled into the entities' constructors.
    logical_entity = LogicalEntity(json_to_parse.get('logicalConfig'))
    graphical_entity = GraphicalEntity(json_to_parse.get('graphicalConfig'))

    return [logical_entity, graphical_entity]


class LogicalEntity(object):

    def __init__(self, config):
        # Take the config and set the object to what is in the config
        self.__dict__.update(config)


class GraphicalEntity(object):

    def __init__(self, config):
        # Take the config and set the object to what is in the config
         self.__dict__.update(config)

