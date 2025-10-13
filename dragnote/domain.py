from __future__ import annotations

import logging
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

    def get_event_value(self) -> int:
        value = self.name.to_num() + self.sign.to_num()
        value += SEMITONES_IN_AN_OCTAVE * self.octave.to_num()
        return value

    def to_events(self, duration: float) -> Iterator[tuple[float, Event]]:
        if self.name == NAME.P:
            pass
        else:
            value = self.get_event_value()

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
    voice: Voice

    def to_events(self) -> Iterator[tuple[float, Event]]:
        for ts, event in self.voice.to_events(self.tempo):
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

    def __eq__(self, other):
        if not isinstance(other, Event):
            raise ValueError(f"Incorrect type: {type(other)}, should be Event")
        if self.value == other.value:
            return True
        return False


@dataclass(frozen=False)
class Schedule:
    values: defaultdict[float, set[Event]]

    def add_event(self, ts: float, event: Event):
        self.values[ts].add(event)

    def __eq__(self, other):
        if not isinstance(other, Schedule):
            raise ValueError(f"Incorrect type: {type(other)}, should be Schedule")
        logger.debug("self, other: %s, %s", self.values, other.values)
        return self.values == other.values

    def __iadd__(self, other: Schedule) -> None:
        if not isinstance(other, Schedule):
            raise ValueError(f"{other} should be a Schedule.")
        for ts, events in other.values.items():
            for event in events:
                self.values[ts].add(event)

    def __add__(self, other: Schedule):
        return NotImplemented

    def get_notes_list(self) -> list[set[int]]:
        keys = list(self.values.keys())
        keys.sort()
        events_on = [{event.value for event in self.values[key] if event.klass == CLASS.ON} for key in keys]
        events_on = [event_on for event_on in events_on if event_on]  # remove None
        return events_on

    def substitute(self, notes_list: list[set[int]]):
        new_values = defaultdict(set)
        keys = list(self.values.keys())
        keys.sort()

        key: float = 0
        old_notes: set[int] = set()
        for key, notes in zip(keys, notes_list, strict=True):
            for old_note in old_notes:
                new_values[key].add(
                    Event(
                        value=old_note,
                        volume=0,
                        klass=CLASS.OFF,
                    )
                )
            old_notes = set()

            for note in notes:
                new_values[key].add(
                    Event(
                        value=note,
                        volume=127,
                        klass=CLASS.ON,
                    )
                )
                old_notes.add(note)

        if old_notes:
            for note in old_notes:
                new_values[key + 1].add(  # key + 1 - fix magic number "1"
                    Event(
                        value=note,
                        volume=0,
                        klass=CLASS.OFF,
                    )
                )

        return Schedule(values=new_values)
