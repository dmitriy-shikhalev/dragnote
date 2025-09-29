import time

import pygame
import pygame.midi

from dragnote.main import FluidSynth
from dragnote.settings import Settings

pygame.midi.init()

settings = Settings()

# Create a MIDI output object
midi_out = pygame.midi.Output(settings.midi_synth_num)


print(pygame.midi.midi_to_ansi_note(48))
midi_out.note_on(12, 127, channel=0)
print(pygame.midi.midi_to_ansi_note(12))
midi_out.note_on(63, 127, channel=0)
midi_out.note_on(67, 127, channel=0)
print(pygame.midi.midi_to_ansi_note(67))

time.sleep(3)

midi_out.note_off(60, 127)
midi_out.note_off(63, 127)
midi_out.note_off(67, 127)
print('stop')


midi_out.close()
pygame.midi.quit()