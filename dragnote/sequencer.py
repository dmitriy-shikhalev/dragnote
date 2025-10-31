import logging

import pygame.midi

from dragnote.domain import Harmony

logger = logging.getLogger(__name__)


class Sequencer:
    def __init__(self, synth_num: int, instrument_num: int, volume: int, tempo: int):
        if synth_num is None:
            raise ValueError("Synth num can not be None!")
        self.synth_num = synth_num
        self.volume = volume
        self.tempo = tempo
        self.midi_out = pygame.midi.Output(synth_num)
        self.midi_out.set_instrument(instrument_num)

    def play_harmony(self, harmony: Harmony, tempo: int):
        logger.debug("play harmony: %s in tempo %s", harmony, tempo)
        for note in harmony.notes:
            self.midi_out.note_on(note.to_note_value(), self.volume)

        pygame.time.wait(
            int(
                harmony.get_duration_in_seconds(tempo) * 1000
            )
        )

        for note in harmony.notes:
            self.midi_out.note_off(note.to_note_value(), self.volume)

    def play_composition(self, composition: list[Harmony]):
        for harmony in composition:
            self.play_harmony(harmony, self.tempo)
