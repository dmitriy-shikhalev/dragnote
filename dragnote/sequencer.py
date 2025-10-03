import logging
import time
from collections import defaultdict

import pygame.midi

from dragnote.domain import Event, Name, Note, note_to_events, Klass, Harmony, Schedule, Voice, duration_to_seconds, \
    Composition, composition_to_schedule

logger = logging.getLogger(__name__)


class Sequencer:
    def __init__(self, synth_num: int):
        self.synth_num = synth_num
        self.midi_out = pygame.midi.Output(synth_num)

    def play_event(self, event: Event):
        if event.klass == Klass.ON:
            logger.debug("Event on: %s", event)
            self.midi_out.note_on(event.value, event.volume)
        else:
            logger.debug("Event off: %s", event)
            self.midi_out.note_off(event.value, event.volume)

    def play_note(self, note: Note, tempo: int):
        for ts, event in note_to_events(note, tempo):
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
        schedule = composition_to_schedule(composition)
        self.play_schedule(schedule)

    def play_schedule(self, schedule: Schedule):
        keys = list(set(schedule.values.keys()))
        keys.sort()
        previous_key = keys[0]
        del keys[0]

        events = schedule.values.pop(previous_key)
        for event in events:
            self.play_event(event)
        for key in keys:
            pygame.time.wait(
                int(
                    (key - previous_key) * 1000
                )
            )
            previous_key = key

            for event in schedule.values.pop(key):
                self.play_event(event)