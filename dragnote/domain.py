from dataclasses import dataclass
from enum import Enum
from numbers import Rational


# Music models

class Name(str, Enum):
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    A = "A"
    H = "H"

    P = "P"  # Pause


@dataclass(frozen=True)
class Note:
    name: Name
    sharp: bool
    flat: bool
    octave: int
    duration: Rational
    volume: int

    def __post_init__(self):
        if self.sharp and self.flat:
            raise ValueError(f"Sharp and flat are both true: {self}")


@dataclass(frozen=True)
class Harmony:
    notes: tuple[Note, ...]


@dataclass(frozen=True)
class Voice:
    harmonies: tuple[Harmony, ...]


@dataclass(frozen=True)
class Composition:
    name: str
    tempo: int
    voices: tuple[Voice, ...]


# Sequenced models

@dataclass(frozen=True)
class Wave:
    value: int
    duration: float
    volume: int


@dataclass(frozen=True)
class Point:
    ts: float
    waves: tuple[Wave, ...]


@dataclass(frozen=True)
class Schedule:
    values: tuple[Point, ...]
