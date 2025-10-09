import pygame.midi

from dragnote.parse import parse_composition
from dragnote.sequencer import Sequencer


def play(composition_name: str, synth_num: int, instrument_num: int):
    pygame.midi.init()
    composition = parse_composition(composition_name)
    sequencer = Sequencer(synth_num, instrument_num)
    sequencer.play_composition(composition)
