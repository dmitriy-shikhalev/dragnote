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

    @classmethod
    def from_str(cls, s: str) -> NAME:
        match s:
            case "C":
                return NAME.C
            case "D":
                return NAME.D
            case "E":
                return NAME.E
            case "F":
                return NAME.F
            case "G":
                return NAME.G
            case "A":
                return NAME.A
            case "H":
                return NAME.H
            case _:
                raise ValueError(s)

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
            case _:
                raise ValueError(self)


class SIGN(str, Enum):
    NATURAL = "NATURAL"
    SHARP = "SHARP"
    FLAT = "FLAT"
    DOUBLE_SHARP = "DOUBLE_SHARP"
    DOUBLE_FLAT = "DOUBLE_FLAT"

    @classmethod
    def from_str(cls, s: str) -> SIGN:
        match s:
            case "":
                return cls.NATURAL
            case "b":
                return cls.FLAT
            case "#":
                return cls.SHARP
            case "bb":
                return cls.DOUBLE_FLAT
            case "##":
                return cls.DOUBLE_FLAT
            case _:
                raise ValueError(s)

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
            case _:
                raise ValueError(self)


class OCTAVE(str, Enum):
    SUBCONTRA = "SUBCONTRA"
    CONTRA = "CONTRA"
    GREAT = "GREAT"
    SMALL = "SMALL"
    FIRST = "FIRST"
    SECOND = "SECOND"
    THIRD = "THIRD"
    FOURTH = "FOURTH"
    FIFTH = "FIFTH"

    @classmethod
    def from_num(cls, num: int) -> OCTAVE:
        match num:
            case -4:
                return cls.SUBCONTRA
            case -3:
                return cls.CONTRA
            case -2:
                return cls.GREAT
            case -1:
                return cls.SMALL
            case 0:
                return cls.FIRST
            case 1:
                return cls.SECOND
            case 2:
                return cls.THIRD
            case 3:
                return cls.FOURTH
            case 4:
                return cls.FIFTH
            case _:
                raise ValueError(num)

    def to_num(self) -> int:
        match self:
            case self.SUBCONTRA:
                return -4
            case self.CONTRA:
                return -3
            case self.GREAT:
                return -2
            case self.SMALL:
                return -1
            case self.FIRST:
                return 0
            case self.SECOND:
                return 1
            case self.THIRD:
                return 2
            case self.FOURTH:
                return 3
            case self.FIFTH:
                return 4
            case _:
                raise ValueError(self)


ACCEPTABLE_ERROR_NUMBER = 3