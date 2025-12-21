"""ЗО модуля - описание и проигрывание спец. звуков в форматах wav или mp3, таких как звук ошибки или звук окончания упражениния."""

from enum import Enum

import pygame


class Sounds(Enum):
    # Bad
    FAIL = "sounds/fail.wav"
    PEEP = "sounds/peep.wav"
    # Good
    OVER = "sounds/over.mp3"
    DZIN = "sounds/dzin.mp3"
    BULK = "sounds/bulk.mp3"


def play_sound(sound: Sounds):
    pygame.mixer.music.load(sound.value)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
