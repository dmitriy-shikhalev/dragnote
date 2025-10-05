import logging
import time
from collections import defaultdict

import pygame.midi

from dragnote.consts import CLASS
from dragnote.domain import (
    Composition,
    Event,
    Harmony,
    Note,
    Schedule,
    Voice,
)

logger = logging.getLogger(__name__)


class Sequencer:
    def __init__(self, synth_num: int):
        self.synth_num = synth_num
        self.midi_out = pygame.midi.Output(synth_num)

    def play_event(self, event: Event):
        if event.klass == CLASS.ON:
            logger.debug("Event on: %s", event)
            self.midi_out.note_on(event.value, event.volume)
        else:
            logger.debug("Event off: %s", event)
            self.midi_out.note_off(event.value, event.volume)

    def play_note(self, note: Note, tempo: int):
        for ts, event in note.to_events(tempo):
            logger.debug("Sleep ts: %s", ts)
            time.sleep(ts)
            logger.debug("play %s", event)
            self.play_event(event)

    def play_harmony(self, harmony: Harmony, tempo: int):
        values = defaultdict(set)

        for note in harmony.notes:
            for ts, event in note_to_events(note, tempo, harmony.duration):
                values[ts].add(event)

        schedule = Schedule(values=values)
        self.play_schedule(schedule)

    def play_voice(self, voice: Voice, tempo: int):
        values = defaultdict(set)
        time_shift = 0

        for harmony in voice.harmonies:
            for note in harmony.notes:
                for ts, event in note_to_events(note, tempo, max_duration=harmony.duration):
                    values[time_shift + ts].add(event)
            time_shift += duration_to_seconds(harmony.duration, tempo)

        schedule = Schedule(values=values)
        self.play_schedule(schedule)

    def play_composition(self, composition: Composition):
        schedule = composition.to_schedule()
        self.play_schedule(schedule)

    def play_schedule(self, schedule: Schedule):
        keys = list(set(schedule.values.keys()))
        keys.sort()
        previous_key = 0

        for key in keys:
            pygame.time.wait(
                int(
                    (key - previous_key) * 1000
                )
            )
            previous_key = key

            for event in schedule.values.pop(key):
                self.play_event(event)