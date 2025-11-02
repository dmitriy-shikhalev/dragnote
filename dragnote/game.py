import logging

from dragnote.domain import Composition, Harmony
from dragnote.parse import parse_notes
from dragnote.queues import InputQueue
from dragnote.sequencer import Sequencer
from dragnote.sounds import Sounds, play_sound

logger = logging.getLogger(__name__)


class Game:
    def __init__(
        self,
        composition: Composition,
        sequencer: Sequencer,
        max_error_count: int,
        volume: int,  # todo: ???
        tempo: int,  # todo: ???
    ):
        self.composition = composition
        self.sequencer = sequencer
        self.max_error_count = max_error_count
        self.volume = volume
        self.tempo = tempo
        self.input_queue = InputQueue()

        self.error_count = 0

    def play(self):
        self.sequencer.play_composition(self.composition)

        it = iter(self.composition)
        while True:
            try:
                harmony = next(it)
            except StopIteration:
                play_sound(Sounds.OVER)
                break

            string = input()
            if not string:
                self.sequencer.play_composition(self.composition)
                continue

            notes = parse_notes(string)
            if set(notes) == set(harmony.notes):
                play_sound(Sounds.DZIN)
                self.sequencer.play_harmony(harmony)
            else:
                play_sound(Sounds.PEEP)
                self.sequencer.play_harmony(harmony)
                self.sequencer.play_harmony(Harmony(notes=tuple(notes), duration=harmony.duration))
                self.error_count += 1
                if self.error_count > self.max_error_count:
                    raise ValueError
