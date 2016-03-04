import os
import pygame.mixer
from .. import settings


now_playing = None


def set_track(track_name):
    global now_playing
    if now_playing == track_name:
        return
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(settings.DATA_DIR, 'music', track_name))
    pygame.mixer.music.play(-1)
    now_playing = track_name
