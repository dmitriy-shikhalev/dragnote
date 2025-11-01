import logging
from fractions import Fraction
from typing import Iterator

from dragnote.domain import Composition, Harmony, Note

logger = logging.getLogger(__name__)


def parse_notes(string: str) -> Iterator[Note]:
    for part in string.split(":"):
        yield Note.from_str(part)


def parse_duration(string: str) -> Fraction:
    if not string or string[0] != "(" or string[-1] != ")":
        raise ValueError(f"Wrong duration string: {string}")
    ls = string[1:-1].split("/")
    numerator = int(ls[0])
    denominator = int(ls[1])
    return Fraction(numerator, denominator)


def parse_composition(txt: str) -> Composition:
    is_note = True
    notes = None
    for part in txt.split():
        if is_note:
            notes = parse_notes(part)
            is_note = False
        else:
            if notes is None:
                raise ValueError("Notes is None, but parsing duration now.")  # pragma: no cover
            duration = parse_duration(part)
            yield Harmony(notes=tuple(notes), duration=duration)
            is_note = True
