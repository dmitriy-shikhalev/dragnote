import logging
import os
from fractions import Fraction
from typing import Iterator

from dragnote.consts import NAME, OCTAVE, SIGN
from dragnote.database import get_filename, get_full_filename
from dragnote.domain import Harmony, Note
from dragnote.errors import NoFile, ParserError

logger = logging.getLogger(__name__)


def parse_note(string: str) -> Note:
    raise NotImplementedError


def parse_notes(string: str) -> Iterator[Note]:
    for part in string.split(":"):
        yield parse_note(part)


def parse_duration(string: str) -> Fraction:
    if not string or string[0] != "(" or string[-1] != ")":
        raise ValueError(f"Wrong duration string: {string}")
    ls = string.split("/")
    numerator = int(ls[0])
    denominator = int(ls[1])
    return Fraction(numerator, denominator)


def parse_composition(num: int) -> Iterator[Harmony]:
    with open(
        get_full_filename(
            get_filename(num)
        )
    ) as fd:
        txt = fd.read()

    is_note = True
    notes = None
    for part in txt.split():
        if is_note:
            notes = parse_notes(part)
            is_note = False
        else:
            if notes is None:
                raise ValueError("Notes is None, but parsing duration now.")
            duration = parse_duration(part)
            yield Harmony(
                notes=tuple(notes),
                duration=duration
            )
            is_note = True

