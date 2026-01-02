"""ЗО модуля - один раунд: считать данные с входа, сравнить с текущими данными упражнения, выдать результат."""

from typing import Iterable

from dragnote.domain import Harmony


class Round:
    def __init__(self, harmonies: Iterable[Harmony]):
        self.harmonies = harmonies

    def run(self) -> tuple[int, int]:
        raise NotImplementedError
