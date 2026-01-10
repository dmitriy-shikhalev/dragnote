"""Зона ответственности модуля - одно уражнение.

Эксерсайз инициализируется композицией. Ран запускает. Умеет проиграть композицию, сравнить ввод с текущей частью
композиции, проиграть запомнить прогресс по композиции, упасть с овер ошибкой, дать текущие правильные гармонии, дать
текущую гармонию, сравнить 2 гармонии, проиграть звук успеха, проиграть звук неудачи, проиграть гармонию с
длительностью.
Нужно добавить класс ИтераторКомпозиции!
"""

import logging
from typing import Sequence

from dragnote.coder import HarmonyCoder
from dragnote.domain import Composition, Harmony
from dragnote.errors import GameOver
from dragnote.play_sounds import (
    play_before_start,
    play_fail,
    play_mistake,
    play_ok,
    play_success,
)
from dragnote.round import Round
from dragnote.sequencer import Sequencer

logger = logging.getLogger(__name__)


class Exercise:
    def __init__(self, composition: Composition, max_error_count: int, sequencer: Sequencer):
        self.composition = composition
        self.max_error_count = max_error_count
        self.sequencer = sequencer
        self.current_harmony = 0
        self.error_count = 0

    def get_harmonies(self) -> Sequence[Harmony]:
        return self.composition.harmonies[self.current_harmony :]

    def get_error_count_string(self):
        return f"{self.error_count}/{self.max_error_count}"

    def get_greeting(self) -> str:
        if self.current_harmony == 0:
            return (
                f"First harmony is {HarmonyCoder.encode(self.composition.harmonies[0].get_without_duration())} "
                f"| {self.get_error_count_string()}"
            )
        return (
            " ".join(
                HarmonyCoder.encode(harmony.get_without_duration())
                for harmony in self.composition.harmonies[: self.current_harmony]
            )
            + f" | {self.get_error_count_string()}"
        )

    def is_over(self) -> bool:
        return self.current_harmony >= len(self.composition.harmonies)

    def is_fail(self) -> bool:
        return self.error_count >= self.max_error_count

    def play_composition(self):
        for harmony in self.composition.harmonies:
            self.sequencer.play_harmony(harmony)

    def run_one_iterate(self):
        logger.critical("New iterate")
        round_ = Round(self.get_harmonies(), greeting=self.get_greeting(), sequencer=self.sequencer)
        count, errors = round_.run()
        if errors:
            self.error_count += 1
            play_mistake()
        elif count:
            play_ok()
        else:
            self.play_composition()
        self.current_harmony += count

    def run(self):
        play_before_start()
        self.play_composition()
        while not self.is_over() and not self.is_fail():
            self.run_one_iterate()

        if self.is_fail():
            play_fail()
            raise GameOver()
        else:
            play_success()
