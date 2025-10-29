import logging
import os
import re
from fractions import Fraction

import yaml

from dragnote.consts import NAME, OCTAVE, SIGN
from dragnote.domain import Note, Harmony
from dragnote.errors import NoFile
from dragnote.regexps import DURATION_INPUT, NOTE_INPUT

logger = logging.getLogger(__name__)
DIRNAME = "compositions"
LIST_FILENAME = "list.yaml"


def get_filename(num: int):
    filenames = yaml.load(open(os.path.join(DIRNAME, LIST_FILENAME)), yaml.Loader)["compositions"]
    if num >= len(filenames):
        raise NoFile(f"No composition with num {num}")
    return filenames[num]


def get_full_filename(filename: str) -> str:
    return os.path.join(DIRNAME, filename)


class ParserError(Exception):
    pass


class Parser:
    result: list[tuple[str]]

    def __init__(self, text: str):
        self.text = text

        # raise ParserError(f"No any result: {self.text}")

    def __iter__(self):
        i = 0
        is_note = True

        notes = []

        for subtext in self.text.split():
            if is_note:
                for note_str in subtext.split(":"):
                    r = NOTE_INPUT.match(note_str)
                    if r is None:
                        raise ParserError(f"Unknown note: {note_str}")
                    groupdict = r.groupdict()
                    notes.append(
                        Note(
                            name=NAME.from_str(groupdict["name"]),
                            sign=SIGN.from_str(groupdict["sign"]),
                            octave=OCTAVE.from_num(int(groupdict["octave"])),
                        ),
                    )

                is_note = False
            else:
                r = DURATION_INPUT.match(subtext)
                if r is None:
                    raise ParserError(f"Wrong duration: {subtext}")
                groupdict = r.groupdict()
                yield Harmony(
                    notes=tuple(notes),
                    duration=Fraction(int(groupdict["beats"]), int(groupdict["duration"]))
                )

                notes.clear()
                is_note = True


def parse_file(filename: str):
    return pydantic_yaml.parse_yaml_file_as(Composition, open(filename))  # type: ignore[type-var]


# def parse_composition(num: int) -> Composition:
#     logger.debug("Get file num %s", num)
#     filename = get_filename(num)
#     logger.debug("Filename: %s", filename)
#     full_filename = get_full_filename(filename)
#     logger.debug("Full filename: %s", full_filename)
#     if not os.path.exists(full_filename):
#         raise NoFile(full_filename)
#     return parse_file(full_filename)
