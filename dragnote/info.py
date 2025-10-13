import logging

import pygame
import pygame.midi

from dragnote.parse import get_compositions

logger = logging.getLogger(__name__)


def print_synths():
    pygame.midi.init()
    for i in range(pygame.midi.get_count()):
        print(f"Midi synth No. {i}: {pygame.midi.get_device_info(i)}")


def print_compositions():
    print("Compositions:")
    for lesson in get_compositions():
        print("*", lesson.name)
