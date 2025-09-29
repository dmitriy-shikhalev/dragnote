import logging

import pygame
import pygame.midi

pygame.midi.init()
logger = logging.getLogger(__name__)


def get_synths():
    for i in range(pygame.midi.get_count()):
        print(f"Midi synth No. {i}: {pygame.midi.get_device_info(i)}")
