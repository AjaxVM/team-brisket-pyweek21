from __future__ import absolute_import, division, print_function, unicode_literals


def process_json(json_to_parse):
    '''
    Takes json from the server or the client and xforms it into a logical entity and a graphical entity
    '''

    logical_entity = LogicalEntity(json_to_parse.get('hit_box_size'), json_to_parse.get('state'))
    graphical_entity = GraphicalEntity(json_to_parse.get('resource'))

    return [logical_entity, graphical_entity]


class LogicalEntity(object):

    def __init__(self, hit_box_size, state):
        # length and width of hit box
        self.hit_box_size = hit_box_size
        self.state = state


class GraphicalEntity(object):

    def __init__(self, resource):
        # Was thinking resource should just be a string of a file location for an image? We can change later
        self.resource = resource

