import pygame

class Resource(object):
    '''
    This class gives you the ability to load a resource.
    Generally, you only need to use get_resource_image,
    but you can use any of the functions in this class to
    work with the resource properties.
    '''
    image_cache = {}
    resource_props = {
        # example for now
        # zombie: {
        #     image: '',
        #     tiles: {
        #         walking_1: (0,0),
        #         walking_2: (0,32)
        #     }
        # },
        'hostile_planet': {
            'image': 'data/assets/hostile_planet_tileset.png',
            'tiles': {
                'red_rock_top_left': (0,0),
                'red_rock_top': (9,0),
                'red_rock_top_right': (24,0),
                'red_rock_left': (0,9),
                'red_rock': (9, 9),
                'red_rock_right': (24, 9),
                'red_rock_bot_left': (0, 24),
                'red_rock_bot': (9, 24),
                'red_rock_bot_right': (24, 24),
            }
        }
    }

    def get_resource_props(self, name):
        """ Grabs resource properties for a specific resource. """
        return self.resource_props[name]

    def get_resource_tile_props(self, name, tile_name):
        """ Grabs tile properties for a specific resource from resource properties. """
        return self.get_resource_props(name)['tiles'][tile_name]

    def load_image(self, name):
        """ Loads an image. """
        if name not in self.image_cache:
            self.image_cache[name] = pygame.image.load(self.get_resource_props(name)['image'])
        return self.image_cache[name]

    def load_tile(self, name, tile_name):
        """ Loads a tile from an image. """
        full_name = name + tile_name
        if full_name not in self.image_cache:
            x, y = self.get_resource_tile_props(name, tile_name)
            self.image_cache[full_name] = self.load_image(name).subsurface(x, y, 24, 24)
        return self.image_cache[full_name]

    def get_resource_image(self, name, tile_name):
        return self.load_tile(name, tile_name)

    def blit(self, screen, name, tile_name, x, y):
        screen.blit(self.get_resource_image(name, tile_name), (x, y))
