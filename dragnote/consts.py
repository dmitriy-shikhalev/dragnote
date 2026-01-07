"""Модуль содержит основные констаты программы."""

from __future__ import annotations

from enum import Enum

SEMITONES_IN_AN_OCTAVE = 12

# Music models


class NAME(Enum):
    """Номер ноты в MIDI в первой (или второй? или третьей?) октаве."""

    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    A = "A"
    H = "H"

    P = 0  # Pause

    def to_num(self) -> int:
        match self:
            case self.C:
                return 60
            case self.D:
                return 62
            case self.E:
                return 64
            case self.F:
                return 65
            case self.G:
                return 67
            case self.A:
                return 69
            case self.H:
                return 71
            case _:  # pragma: no cover
                raise ValueError(self)


class SIGN(str, Enum):
    NATURAL = "NATURAL"
    SHARP = "SHARP"
    FLAT = "FLAT"
    DOUBLE_SHARP = "DOUBLE_SHARP"
    DOUBLE_FLAT = "DOUBLE_FLAT"

    def to_num(self) -> int:
        match self:
            case self.NATURAL:
                return 0
            case self.FLAT:
                return -1
            case self.SHARP:
                return 1
            case self.DOUBLE_FLAT:
                return -2
            case self.DOUBLE_SHARP:
                return 2
            case _:  # pragma: no cover
                raise ValueError(self)


class OCTAVE(str, Enum):
    SMALL = "SMALL"
    FIRST = "FIRST"
    SECOND = "SECOND"

    def to_num(self) -> int:
        match self:
            case self.SMALL:
                return 0
            case self.FIRST:
                return 1
            case self.SECOND:
                return 2
            case _:  # pragma: no cover
                raise ValueError(self)


ACCEPTABLE_ERROR_NUMBER = 3

FILENAME = "_current.db"
DIRNAME = "compositions"
LIST_FILENAME = "list.yaml"
