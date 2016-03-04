import pygame

class Resource(Object):
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
                'red_rock_top': (32,0),
                'red_rock_top_right': (64,0),
                'red_rock_left': (0,32),
                'red_rock': (32,32),
                'red_rock_right': (64,32),
                'red_rock_bot_left': (64,0),
                'red_rock_bot': (64,32),
                'red_rock_bot_right': (64,64)
            }
        }
    }

    def get_resource_props(self, name):
        ''' Grabs resource properties for a specific resource. '''
        return self.resource_props[name]

    def get_resource_tile_props(self, name, tile_name):
        ''' Grabs tile properties for a specific resource from resource properties. '''
        return self.get_resource_props(name).tiles[tile_name]

    def load_image(self, name):
        ''' Loads an image. '''
        if not self.image_cache[name]:
            self.image_cache[name] = pygame.transform.scale2x(
                pygame.image.load(self.get_resource_props(name).image)
            )

        return self.image_cache[name]

    def load_tile(self, name, tile_name):
        full_name = name + tile_name
        ''' Loads a tile from an image. '''
        if not self.image_cache[full_name]:
            tile_props_tuple = self.get_resource_tile_props(name, tile_name)
            # self.image_cache[full_name] = pygame.transform.chop(
            #     load_image(name),
            #     pygame.Rect(tile_props_tuple[0], tile_props_tuple[1], 32, 32)
            # )
            self.image_cache[full_name] = self.load_image(name).subsurface(
                tile_props_tuple[0],
                tile_props_tuple[1],
                32,32
            )

        return self.image_cache[full_name]

    def get_resource_image(self, name, tile_name):
        return self.load_tile(name, tile_name)