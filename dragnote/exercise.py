"""Зона ответственности модуля - одно уражнение.

Эксерсайз инициализируется композицией. Ран запускает. Умеет проиграть композицию, сравнить ввод с текущей частью
композиции, проиграть запомнить прогресс по композиции, упасть с овер ошибкой, дать текущие правильные гармонии, дать
текущую гармонию, сравнить 2 гармонии, проиграть звук успеха, проиграть звук неудачи, проиграть гармонию с
длительностью.
Нужно добавить класс ИтераторКомпозиции!
"""

from typing import Iterable

from dragnote.domain import Composition, Harmony
from dragnote.errors import GameOver
from dragnote.play_sounds import (
    play_before_start,
    play_fail,
    play_mistake,
    play_success,
)
from dragnote.round import Round


class Exercise:
    def __init__(self, composition: Composition, max_error_count: int):
        self.composition = composition
        self.max_error_count = max_error_count
        self.current_harmony = 0
        self.error_count = 0

    def get_harmonies(self) -> Iterable[Harmony]:
        return self.composition.harmonies[self.current_harmony :]

    def is_over(self) -> bool:
        return self.current_harmony >= len(self.composition.harmonies)

    def is_fail(self) -> bool:
        return self.error_count >= self.max_error_count

    def run_one_iterate(self):
        round_ = Round(self.get_harmonies())
        count, errors = round_.run()
        if errors:
            self.error_count += 1
            play_mistake()
        self.current_harmony += count

    def run(self):
        play_before_start()
        while not self.is_over():
            self.run_one_iterate()

        if self.is_fail():
            play_fail()
            raise GameOver()
        else:
            play_success()
