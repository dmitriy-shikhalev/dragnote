import logging
from fractions import Fraction

from dragnote.consts import ACCEPTABLE_ERROR_NUMBER
from dragnote.database import read, write
from dragnote.domain import Composition, Harmony, Note
from dragnote.parse import parse_composition
from dragnote.sequencer import Sequencer
from dragnote.sounds import Sounds, play_sound

logger = logging.getLogger(__name__)


def get_notes_list_from_str(input_notes: str, duration: Fraction) -> list[Note]:
    note_list = Harmony.from_str(input_notes, duration)
    note_list = [s for s in note_list.notes if s]  # todo: use normal name against "s"
    return note_list


class PlayHarmony:
    def __init__(self, harmony: Harmony, count: int, step_num: int, tempo: int, sequencer: Sequencer):
        self.harmony = harmony
        self.count = count
        self.step_num = step_num
        self.tempo = tempo
        self.sequencer = sequencer

    def play(self, tail: str) -> tuple[bool, str]:
        while self.count:
            if not tail:
                print("Step", self.step_num)
                input_notes = input(f"tries left: {self.count}: ")
                if " " in input_notes:
                    input_notes, tail = input_notes.split(" ", 1)
                else:
                    tail = ""
            else:
                if " " in tail:
                    input_notes, tail = tail.split(" ", 1)
                else:
                    input_notes = tail
                    tail = ""
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
                return True, tail
            else:
                play_sound(Sounds.PEEP)
                self.sequencer.play_harmony(self.harmony, tempo=self.tempo)
                self.count -= 1
        return False, tail


class PlayComposition:
    def __init__(self, composition_num: int, sequencer: Sequencer):
        self.composition_num = composition_num
        self.sequencer = sequencer
        self.composition = parse_composition(self.composition_num)

    def get_harmonies(self):
        for harmony in self.composition.harmonies:
            yield harmony

    def play(self):
        print("Composition name is", self.composition.name)
        print("Tonality is", self.composition.tonality)
        self.sequencer.play_composition(self.composition)
        tail = []

        for i, harmony in enumerate(self.get_harmonies()):
            play_harmony = PlayHarmony(harmony, ACCEPTABLE_ERROR_NUMBER, i, self.composition.tempo, self.sequencer)
            result, tail = play_harmony.play(tail)

            if result:
                play_sound(Sounds.OVER)
            else:
                play_sound(Sounds.FAIL)
                break
        else:
            play_sound(Sounds.BULK)
            write(self.composition_num + 1)


def play(synth_num: int):
    sequencer = Sequencer(synth_num, 0)

    while True:
        composition_num = read()

        try:
            play_composition = PlayComposition(composition_num, sequencer)
        except ValueError:
            print(f"No composition {composition_num}")
            play_sound(Sounds.DZIN)
            return

        play_composition.play()
