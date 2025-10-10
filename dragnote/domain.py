from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterator

from dragnote.consts import (
    CLASS,
    NAME,
    OCTAVE,
    SEMITONES_IN_AN_OCTAVE,
    SIGN,
)


@dataclass(frozen=True)
class Note:
    name: NAME
    sign: SIGN
    octave: OCTAVE
    volume: int

    def __eq__(self, other: Note):
        if self._get_event_value() != other._get_event_value():
            return False
        return True

    @classmethod
    def from_str(cls, s: str) -> Note:
        if len(s) < 2:
            raise ValueError(f"Too short str: {s}")
        name = NAME.from_str(s[0])

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

    def _get_event_value(self) -> int:
        value = self.name.to_num() + self.sign.to_num()
        value += SEMITONES_IN_AN_OCTAVE * self.octave.to_num()
        return value

    def to_events(self, duration: float) -> Iterator[tuple[float, Event]]:
        if self.name == NAME.P:
            pass
        else:
            value = self._get_event_value()

            yield 0, Event(value=value, volume=self.volume, klass=CLASS.ON)
            yield duration, Event(value=value, volume=self.volume, klass=CLASS.OFF)


@dataclass(frozen=True)
class Harmony:
    notes: tuple[Note, ...]
    duration: Fraction

    def get_duration_in_seconds(self, tempo: int) -> float:
        return float(self.duration) * 4 * 60 / tempo

    def to_events(self, tempo: int) -> Iterator[tuple[float, Event]]:
        for note in self.notes:
            for ts, event in note.to_events(self.get_duration_in_seconds(tempo)):
                yield ts, event


@dataclass(frozen=True)
class Voice:
    harmonies: tuple[Harmony, ...]

    def to_events(self, tempo: int) -> Iterator[tuple[float, Event]]:
        offset: float = 0
        for harmony in self.harmonies:
            for ts, event in harmony.to_events(tempo):
                yield ts + offset, event

            offset += harmony.get_duration_in_seconds(tempo)


@dataclass(frozen=True)
class Composition:
    name: str
    tempo: int
    tonality: str
    voices: tuple[Voice, ...]

    def to_events(self) -> Iterator[tuple[float, Event]]:
        for voice in self.voices:
            for ts, event in voice.to_events(self.tempo):
                yield ts, event

    def to_schedule(self) -> Schedule:
        # Or, may be, this method need to be moved in class @classmethod Schedule.from_composition(cls, composition)?
        schedule = Schedule(values=defaultdict(set))
        for ts, event in self.to_events():
            schedule.add_event(ts, event)
        return schedule


# Sequenced models


@dataclass(frozen=True)
class Event:
    value: int
    volume: int
    klass: CLASS


@dataclass(frozen=False)
class Schedule:
    values: defaultdict[float, set[Event]]

    def add_event(self, ts: float, event: Event):
        self.values[ts].add(event)

    def __iadd__(self, other: Schedule) -> None:
        if not isinstance(other, Schedule):
            raise ValueError(f"{other} should be a Schedule.")
        for ts, events in other.values.items():
            for event in events:
                self.values[ts].add(event)

    def __add__(self, other: Schedule):
        return NotImplemented

    def substitute(self, notes: Iterator[set[Note]]) -> Schedule:
        raise NotImplementedError
