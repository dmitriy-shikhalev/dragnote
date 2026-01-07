"""Зона ответственности модуля - классы специфичных ошибок."""


class NoFile(Exception):
    pass


class CoderError(Exception):
    pass


class GameOver(Exception):
    pass


class EmptyInput(Exception):
    pass
