import logging
from fractions import Fraction

from dragnote.consts import ACCEPTABLE_ERROR_NUMBER
from dragnote.database import read, write
from dragnote.domain import Harmony, Note
from dragnote.errors import NoFile
from dragnote.parse import parse_composition, parse_note
from dragnote.sequencer import Sequencer
from dragnote.sounds import Sounds, play_sound

logger = logging.getLogger(__name__)


class Game:
    def __init__(
        self,
        composition: list[Harmony],
        sequencer: Sequencer,
        max_error_count: int,
        composition_num: int,
        volume: int,
        tempo: int,
    ):
        self.composition = composition
        self.sequencer = sequencer
        self.max_error_count = max_error_count
        self.error_count = 0

    def play(self):
        raise NotImplementedError


class PlayHarmony:
    def __init__(self, harmony: Harmony, count: int, step_num: int, tempo: int, sequencer: Sequencer):
        self.harmony = harmony
        self.count = count
        self.step_num = step_num
        self.tempo = tempo
        self.sequencer = sequencer
        self.input = input

    def play(self) -> bool:
        while self.count:
            input_notes = self.input.get_note()
            try:
                new_harmony = Harmony.from_str(input_notes, self.harmony.duration)
            except ValueError as error:
                logger.debug(error)
                print(f"Incorrect input: {error.args[0]}")
                continue

            values = {note.to_note_value() for note in self.harmony.notes}
            input_values = {note.to_note_value() for note in new_harmony.notes}
            result = values == input_values
            self.sequencer.play_harmony(new_harmony, tempo=self.tempo)
            if result:
                return True
            else:
                play_sound(Sounds.PEEP)
                self.input.clean()
                self.sequencer.play_harmony(self.harmony, tempo=self.tempo)
                self.count -= 1
        return False


class PlayComposition:
    _composition: list[Harmony] | None = None

    def __init__(self, composition_num: int, sequencer: Sequencer, volume: int, tempo: int):
        self.composition_num = composition_num
        self.sequencer = sequencer
        self.volume = volume
        self.tempo = tempo

    @property
    def composition(self):
        if self._composition is None:
            self._composition = parse_composition(self.composition_num)
        return self._composition

    def get_harmonies(self):
        for harmony in self.composition:
            yield harmony

    def play(self):
        logger.debug("Play composition")
        print("New composition")
        print("First note is", self.composition[0].notes)
        self.sequencer.play_composition(self.composition)
        input_ = Input()

        for i, harmony in enumerate(self.get_harmonies()):
            play_harmony = PlayHarmony(harmony, ACCEPTABLE_ERROR_NUMBER, i, self.tempo, self.sequencer, input_)
            result = play_harmony.play()

            if not result:
                play_sound(Sounds.FAIL)
                break
            input_.right_notes.append(harmony.to_str())
        else:
            play_sound(Sounds.BULK)
            write(self.composition_num + 1)
