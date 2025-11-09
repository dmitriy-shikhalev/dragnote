import logging
from queue import Queue
from typing import Iterator

from dragnote.domain import Composition, Harmony, Note
from dragnote.errors import EmptyInput, GameOver
from dragnote.iofuncs import play_mistake, play_ok, play_over, read_input
from dragnote.parse import parse_notes
from dragnote.queues import InputQueue
from dragnote.sequencer import Sequencer

logger = logging.getLogger(__name__)


class Game:
    def __init__(
        self,
        composition: Composition,
        sequencer: Sequencer,
        max_error_count: int,
        volume: int,
        tempo: int,
    ):
        self.composition = composition
        self.sequencer = sequencer
        self.max_error_count = max_error_count
        self.volume = volume
        self.tempo = tempo
        self.input_queue = InputQueue()
        self.queue: Queue[Harmony] = Queue()
        self._init_queue()

        self.error_count = 0

    def _play_composition(self):
        self.sequencer.play_composition(self.composition)

    def _init_queue(self):
        for harmony in self.composition:
            self.queue.put(harmony)

    def _ok(self, harmony: Harmony):
        play_ok()
        self.sequencer.play_harmony(harmony)
        self.error_count = 0

    def _mistake(self, harmony: Harmony, notes: Iterator[Note]):
        self.queue.put(harmony)
        play_mistake()
        self.sequencer.play_harmony(harmony)
        self.sequencer.play_harmony(Harmony(notes=tuple(notes), duration=harmony.duration))
        self.error_count += 1
        if self.error_count > self.max_error_count:
            raise GameOver

    @staticmethod
    def _read_input():
        string = read_input()
        if not string:
            raise EmptyInput
        return string

    def _get_notes(self) -> Iterator[Note]:
        string = self._read_input()
        notes = parse_notes(string)
        return notes

    @staticmethod
    def _is_harmony_eq_notes(harmony: Harmony, notes: Iterator[Note]):
        return set(notes) == set(harmony.notes)

    def _one_iterate_play(self):
        try:
            notes = self._get_notes()
        except EmptyInput:
            self._play_composition()
            return

        harmony = self.queue.get()
        if self._is_harmony_eq_notes(harmony, notes):
            self._ok(harmony)
        else:
            self._mistake(harmony, notes)

    def play(self):
        self._play_composition()

        while True:
            if not self.queue.qsize():
                play_over()
                break

            self._one_iterate_play()
