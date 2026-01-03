"""ЗО модуля - обеспечить точку входа в программу из терминала."""

import logging

import pygame.midi

from dragnote.game import Game
from dragnote.settings import Settings


def main():
    settings = Settings()

    logging.basicConfig(level=getattr(logging, settings.log_level))

    game_instance = Game(settings)
    game_instance.run()


def synths():
    pygame.init()
    pygame.midi.init()
    count = pygame.midi.get_count()
    print("Count of synths is", count)
    for i in range(count):
        info = pygame.midi.get_device_info(i)
        print(i, info)

