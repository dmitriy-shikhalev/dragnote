"""
ЗО модуля - инициализация музыкальных МИДИ библиотек в начале выполениня программы.
"""

import pygame
import pygame.midi


def initialize():
    pygame.init()
    pygame.mixer.init()
    pygame.midi.init()
