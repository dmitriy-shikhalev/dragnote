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

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Note:
    name: NAME
    sign: SIGN
    octave: OCTAVE

    def __eq__(self, other: object):
        if not isinstance(other, Note):
            raise ValueError(f"Can not check equality Note and {other}")
        return self.to_value() == other.to_value()

    def to_value(self) -> int:
        value = self.name.to_num() + self.sign.to_num()
        value += SEMITONES_IN_AN_OCTAVE * self.octave.to_num()
        return value


@dataclass(frozen=True)
class Duration:
    numerator: int
    denominator: int

    def to_fraction(self) -> Fraction:
        return Fraction(self.numerator, self.denominator)


@dataclass(frozen=True)
class Harmony:
    notes: tuple[Note, ...]
    duration: Duration | None = None

    def __eq__(self, other):
        if not isinstance(other, Harmony):
            raise ValueError(f"Can not compare Harmony ({self}) and {type(other)} ({other})")
        if set(self.notes) != set(other.notes):
            return False
        return True

    def get_duration_in_seconds(self, tempo: int) -> float:
        if self.duration is None:
            raise ValueError("No duration")
        return float(self.duration.to_fraction()) * 60 / tempo

    def get_without_duration(self) -> Harmony:
        return Harmony(
            notes=self.notes,
            duration=None,
        )


@dataclass(frozen=True)
class Composition:
    harmonies: tuple[Harmony, ...]


@dataclass
class Info:
    common: int
    current: int
    attempts: int
