from __future__ import annotations

import logging
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterator

from dragnote.consts import (
    NAME,
    OCTAVE,
    SEMITONES_IN_AN_OCTAVE,
    SIGN,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Note:
    name: NAME
    sign: SIGN
    octave: OCTAVE

    def __eq__(self, other: object):
        if not isinstance(other, Note):
            raise ValueError(f"Can not check equality Note and {other}")
        return self.to_note_value() == other.to_note_value()

    @classmethod
    def from_str(cls, string: str) -> Note:
        name = NAME.from_str(string[0])
        sign = SIGN.from_str(string[1:-1])
        octave = OCTAVE.from_num(int(string[-1]))

        return Note(name=name, sign=sign, octave=octave)

    def to_note_value(self) -> int:
        value = self.name.to_num() + self.sign.to_num()
        value += SEMITONES_IN_AN_OCTAVE * self.octave.to_num()
        return value

    def to_str(self) -> str:
        return f"{self.name.value}{self.sign.to_str()}{self.octave.to_num()}"


@dataclass(frozen=True)
class Harmony:
    notes: tuple[Note, ...]
    duration: Fraction

    @classmethod
    def from_str(cls, s: str, duration: Fraction) -> Harmony:
        return Harmony(notes=tuple(Note.from_str(note_str) for note_str in s.split(":")), duration=duration)

    def get_duration_in_seconds(self, tempo: int) -> float:
        return float(self.duration) * 4 * 60 / tempo

    def to_str(self) -> str:
        return ":".join([note.to_str() for note in self.notes])


Composition = Iterator[Harmony]
