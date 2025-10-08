from enum import Enum

SEMITONES_IN_AN_OCTAVE = 12
OCTAVE_SHIFT = 3

# Music models


class NAME(int, Enum):
    """Номер ноты в MIDI в первой (или второй? или третьей?) октаве."""

    C = 60
    D = 62
    E = 64
    F = 65
    G = 67
    A = 69
    H = 71

    P = 0  # Pause


class SIGN(int, Enum):
    NATURAL = 0
    SHARP = 1
    FLAT = -1
    DOUBLE_SHARP = 2
    DOUBLE_FLAT = -2


class CLASS(str, Enum):
    ON = "ON"
    OFF = "OFF"


class OCTAVE(str, Enum):
    SUBCONTRA = -1
    CONTRA = 0
    GREAT = 1
    SMALL = 2
    FIRST = 3
    SECOND = 4
    THIRD = 5
    FOURTH = 6
    FIFTH = 7
