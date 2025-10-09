import logging

import pygame.midi

from dragnote.consts import CLASS
from dragnote.domain import (
    Composition,
    Event,
    Schedule,
)

logger = logging.getLogger(__name__)


class Sequencer:
    def __init__(self, synth_num: int, instrument_num: int):
        if synth_num is None:
            raise ValueError("Synth num can not be None!")
        self.synth_num = synth_num
        self.midi_out = pygame.midi.Output(synth_num)
        self.midi_out.set_instrument(instrument_num)

    def play_event(self, event: Event):
        if event.klass == CLASS.ON:
            logger.debug("Event on: %s", event)
            self.midi_out.note_on(event.value, event.volume)
        else:
            logger.debug("Event off: %s", event)
            self.midi_out.note_off(event.value, event.volume)

    def play_composition(self, composition: Composition):
        schedule = composition.to_schedule()
        self.play_schedule(schedule)

    def play_schedule(self, schedule: Schedule):
        keys = list(set(schedule.values.keys()))
        keys.sort()
        previous_key: float = 0

        for key in keys:
            pygame.time.wait(int((key - previous_key) * 1000))
            previous_key = key

            for event in schedule.values.pop(key):
                self.play_event(event)
