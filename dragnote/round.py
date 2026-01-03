"""ЗО модуля - один раунд: считать данные с входа, сравнить с текущими данными упражнения, выдать результат."""

from typing import Sequence

from dragnote.compare import Compare
from dragnote.domain import Harmony
from dragnote.iofuncs import read_notes
from dragnote.play_sounds import play_mistake
from dragnote.sequencer import Sequencer


class Round:
    def __init__(self, harmonies: Sequence[Harmony], greeting: str, sequencer: Sequencer):
        self.harmonies = harmonies
        self.greeting = greeting
        self.sequencer = sequencer

    def play_harmonies(self):
        for harmony in self.harmonies:
            self.sequencer.play_harmony(harmony)

    def run(self) -> tuple[int, int]:
        self.play_harmonies()

        composition = read_notes(self.greeting)
        count = 0
        errors = 0

        while count < len(self.harmonies):
            compare = Compare(self.harmonies[count], composition.harmonies[count])
            if compare.is_equal():
                self.sequencer.play_harmony(composition.harmonies[count])
                count += 1
            else:
                self.sequencer.play_harmony(self.harmonies[count])
                play_mistake()
                errors += 1
                break

        return count, errors
