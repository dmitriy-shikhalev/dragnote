from __future__ import annotations

from enum import Enum

SEMITONES_IN_AN_OCTAVE = 12

# Music models


class NAME(Enum):
    """Номер ноты в MIDI в первой (или второй? или третьей?) октаве."""

    C = "C"
    D = 62
    E = 64
    F = 65
    G = 67
    A = 69
    H = 71

    P = 0  # Pause

    @classmethod
    def from_str(cls, s: str) -> NAME:
        match s:
            case "C":
                return NAME.C
            case _:
                raise ValueError(s)

    def to_num(self) -> int:
        match self:
            case self.C:
                return 60
            case _:
                raise ValueError(self)


class SIGN(str, Enum):
    NATURAL = "NATURAL"
    SHARP = 1
    FLAT = -1
    DOUBLE_SHARP = 2
    DOUBLE_FLAT = -2

    @classmethod
    def from_str(cls, s: str) -> SIGN:
        match s:
            case "":
                return SIGN.NATURAL
            case _:
                raise ValueError(s)

    def to_num(self) -> int:
        match self:
            case self.NATURAL:
                return 0
            case _:
                raise ValueError(self)


class OCTAVE(str, Enum):
    SUBCONTRA = -1
    CONTRA = 0
    GREAT = 1
    SMALL = 2
    FIRST = "FIRST"
    SECOND = 4
    THIRD = 5
    FOURTH = 6
    FIFTH = 7

    @classmethod
    def from_num(cls, num: int) -> OCTAVE:
        match num:
            case 0:
                return cls.FIRST
            case _:
                raise ValueError(num)

    def to_num(self) -> int:
        match self:
            case self.FIRST:
                return 0
            case _:
                raise ValueError(self)


# Events


class CLASS(str, Enum):
    ON = "ON"
    OFF = "OFF"
