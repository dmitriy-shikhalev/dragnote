"""Модель отвечает за модели предметной области программы."""

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
from dragnote.regexp import NOTE_DURATION_RE

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
        r = NOTE_DURATION_RE.match(string)
        if not r:
            raise ValueError(f"Not correct note: {string}")
        name = NAME.from_str(r.groupdict()["name"])
        sign = SIGN.from_str(r.groupdict()["sign"])
        octave = OCTAVE.from_num(int(r.groupdict()["octave"]))

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
    duration: Fraction | None = None

    @classmethod
    def from_str(cls, s: str, duration: Fraction | None = None) -> Harmony:
        if duration:
            return Harmony(notes=tuple(Note.from_str(note_str) for note_str in s.split(":")), duration=duration)

        value = NOTE_DURATION_RE.match(s)
        if not value:
            raise ValueError(f"Not a Harmony: {s}")
        return Harmony(
            notes=tuple(Note.from_str(note_str) for note_str in value.groupdict()["notes"].split(":")),
            duration=Fraction(value.groupdict()["duration"]),
        )

    def __eq__(self, other):
        if not isinstance(other, Harmony):
            raise ValueError(f"Can not compare Harmony ({self}) and {type(other)} ({other})")
        if set(self.notes) != set(other.notes):
            return False
        return True

    def get_duration_in_seconds(self, tempo: int) -> float:
        if self.duration is None:
            raise ValueError("No duration")
        return float(self.duration) * 60 / tempo

    def to_str(self) -> str:
        return ":".join([note.to_str() for note in self.notes])


@dataclass(frozen=True)
class Composition:
    harmonies: tuple[Harmony, ...]

    @classmethod
    def from_str(cls, s: str) -> Composition:
        ls = s.split()
        harmonies = []
        for st in ls:
            harmony = Harmony.from_str(st, 1)
            harmonies.append(harmony)
        return cls(harmonies=tuple(harmonies))


@dataclass
class Info:
    common: int
    current: int
    attempts: int
