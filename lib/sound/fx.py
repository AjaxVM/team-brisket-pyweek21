import os
import random
import pygame.mixer
try:
    import numpy as np
    import pygame.sndarray
    has_array = True
except ImportError:
    has_array = False
from .. import settings


class SoundCache(dict):
    def __missing__(self, sound_name):
        sound = pygame.mixer.Sound(os.path.join(settings.DATA_DIR, 'music', sound_name))
        options = [sound]
        if not has_array:
            return options
        base_sample = pygame.sndarray.array(sound)
        for factor in (0.98, 0.99, 1.01, 1.02):
            new_sample = change_pitch(base_sample, factor)
            options.append(pygame.sndarray.make_sound(new_sample))
        return options


SOUND_CACHE = SoundCache()


def playfx(sound_name):
    sound = random.choice(SOUND_CACHE[sound_name])
    sound.play()


def change_pitch(sound_array, factor):
    indices = np.round(np.arange(0, len(sound_array), factor))
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[indices.astype(int)]
