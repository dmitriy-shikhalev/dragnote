from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction

from attr.validators import max_len


# Music models

class Name(int, Enum):
    """
    Номер ноты в MIDI в первой (или второй? или третьей?) октаве.
    """
    C = 60
    D = 62
    E = 64
    F = 65
    G = 67
    A = 69
    H = 71

    P = 0  # Pause


class Sign(int, Enum):
    NATURAL = 0
    SHARP = 1
    FLAT = -1
    DOUBLE_SHARP = 2
    DOUBLE_FLAT = -2



@dataclass(frozen=True)
class Note:
    name: Name
    sign: Sign
    octave: int
    duration: Fraction
    volume: int

    @property
    def value(self) -> int:
        value = self.name.value + self.sign.value

        value += 12 * (self.octave - 3)
        return value


@dataclass(frozen=True)
class Harmony:
    notes: tuple[Note, ...]
    duration: Fraction


@dataclass(frozen=True)
class Voice:
    harmonies: tuple[Harmony, ...]


@dataclass(frozen=True)
class Composition:
    name: str
    tempo: int
    tonality: str
    voices: tuple[Voice, ...]

    def to_schedule(self):
        raise NotImplementedError


# Sequenced models

class Klass(str, Enum):
    ON = "ON"
    OFF = "OFF"


@dataclass(frozen=True)
class Event:
    value: int
    volume: int
    klass: Klass


@dataclass(frozen=True)
class Schedule:
    values: dict[float, set[Event]]

    def __sum__(self, other: Schedule) -> Schedule:
        if not isinstance(other, Schedule):
            raise ValueError(f"{other} should be a Schedule.")
        new_values = defaultdict(set)
        for ts, events in self.values.items():
            for event in events:
                new_values[ts].add(event)
        return Schedule(values=new_values)


def duration_to_seconds(duration: Fraction, tempo: int) -> float:
    return float(duration) * 4 * 60 / tempo


def note_to_events(
    note: Note, tempo: int, max_duration: Fraction | None = None
) -> tuple[tuple[float, Event], tuple[float, Event]]:
    """
    duration_in_seconds = duration_in_fractal * 60 / tempo
    """
    if note.name == Name.P:
        return ()

    if max_duration is None:
        duration = duration_to_seconds(note.duration, tempo)
    else:
        duration = duration_to_seconds(max_duration, tempo)

    return (
        (
            0,
            Event(
                value=note.value,
                volume=note.volume,
                klass=Klass.ON,
            ),
        ),
        (
            duration,
            Event(
                value=note.value,
                volume=note.volume,
                klass=Klass.OFF,
            )
        )
    )


def harmony_to_schedule(harmony: Harmony) -> Schedule:
    raise NotImplementedError


def voice_to_schedule(voice: Voice) -> Schedule:
    raise NotImplementedError


def composition_to_schedule(composition: Composition) -> Schedule:
    schedules = [voice_to]
