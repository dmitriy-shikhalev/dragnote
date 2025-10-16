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
    volume: int

    @classmethod
    def from_str(cls, s: str) -> Note:
        if len(s) < 2:
            raise ValueError(f"Too short str: {s}")
        name = NAME.from_str(s[0].upper())

        octave_num = int(s[-1])
        if s[-2] == "-":
            octave_num *= -1
        octave = OCTAVE.from_num(octave_num)

        sign_str = s[1:-1] if octave_num >= 0 else s[1:-2]
        sign = SIGN.from_str(sign_str)
        return cls(
            name=name,
            sign=sign,
            octave=octave,
            volume=127,  # это заведомо ложное значение, но оно не играет роли, потому что планируется использовать ноты из этого метода лишь для сравнения.
        )

    def to_note_value(self) -> int:
        value = self.name.to_num() + self.sign.to_num()
        value += SEMITONES_IN_AN_OCTAVE * self.octave.to_num()
        return value


@dataclass(frozen=True)
class Harmony:
    notes: tuple[Note, ...]
    duration: Fraction

    def get_duration_in_seconds(self, tempo: int) -> float:
        return float(self.duration) * 4 * 60 / tempo


@dataclass(frozen=True)
class Voice:
    harmonies: tuple[Harmony, ...]


@dataclass(frozen=True)
class Composition:
    name: str
    tempo: int
    tonality: str
    voice: Voice
