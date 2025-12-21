"""Зона ответственности модуля - классы специфичных ошибок."""

class NoFile(Exception):
    pass


class ParserError(Exception):
    pass


class GameOver(Exception):
    pass


class EmptyInput(Exception):
    pass
