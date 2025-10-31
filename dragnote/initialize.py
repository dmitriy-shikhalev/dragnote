import pygame
import pygame.midi


def initialize_midi():
    pygame.init()
    pygame.mixer.init()
    pygame.midi.init()
