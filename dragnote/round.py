"""ЗО модуля - один раунд: считать данные с входа, сравнить с текущими данными упражнения, выдать результат."""

import logging
from typing import Sequence

from dragnote.compare import Compare
from dragnote.domain import Harmony
from dragnote.iofuncs import read_notes
from dragnote.sequencer import Sequencer

logger = logging.getLogger(__name__)


class Round:
    def __init__(self, harmonies: Sequence[Harmony], greeting: str, sequencer: Sequencer):
        self.harmonies = harmonies
        self.greeting = greeting
        self.sequencer = sequencer

    def run(self) -> tuple[int, int]:
        composition = read_notes(self.greeting)
        count = 0
        errors = 0

        while count < len(self.harmonies) and count < len(composition.harmonies):
            logger.debug("Play %s note in harmonies, len(self.harmonies) = %s", count, len(self.harmonies))
            compare = Compare(self.harmonies[count], composition.harmonies[count])
            if compare.is_equal():
                self.sequencer.play_harmony(self.harmonies[count])
                count += 1
            else:
                self.sequencer.play_harmony(
                    composition.harmonies[count].get_with_duration(self.harmonies[count].duration)
                )
                errors += 1
                break

        return count, errors
