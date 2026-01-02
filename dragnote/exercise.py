"""Зона ответственности модуля - одно уражнение.

Эксерсайз инициализируется композицией. Ран запускает. Умеет проиграть композицию, сравнить ввод с текущей частью
композиции, проиграть запомнить прогресс по композиции, упасть с овер ошибкой, дать текущие правильные гармонии, дать
текущую гармонию, сравнить 2 гармонии, проиграть звук успеха, проиграть звук неудачи, проиграть гармонию с
длительностью.
Нужно добавить класс ИтераторКомпозиции!
"""

from dragnote.domain import Composition
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

    def run(self):
        play_before_start()
        while self.current_harmony < len(self.composition.harmonies):
            round_ = Round(self.composition.harmonies[self.current_harmony :])
            count, errors = round_.run()
            if errors:
                self.error_count += 1
                play_mistake()
            self.current_harmony += count

        if self.current_harmony >= self.max_error_count:
            play_fail()
            raise GameOver()
        else:
            play_success()
