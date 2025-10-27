from __future__ import annotations

import logging
from dataclasses import dataclass
from fractions import Fraction

from dragnote.consts import (
    NAME,
    OCTAVE,
    SEMITONES_IN_AN_OCTAVE,
    SIGN,
)
from dragnote.regexps import NOTE_INPUT

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Note:
    name: NAME
    sign: SIGN
    octave: OCTAVE

    @classmethod
    def from_str(cls, s: str) -> Note:
        r = NOTE_INPUT.search(s)
        if r is None:
            raise ValueError(f"Incorrect note: \"{s}\"")

        groupdict = r.groupdict()
        name = NAME.from_str(groupdict["note"].upper())
        sign = SIGN.from_str(groupdict["sign"] or "")
        octave = OCTAVE.from_num(int(groupdict["octave"]))

        return cls(
            name=name,
            sign=sign,
            octave=octave,
        )

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


@dataclass(frozen=True)
class Composition:
    tempo: int
    first_note: str
    harmonies: tuple[Harmony, ...]
