import re

regexp = re.compile("(?P<symbol>[ACDEFGHacdefghBb#]+)(?P<octave>[0123456789-]+)")
_notes = {
    "c": 60,
    "c#": 61,
    "db": 61,
    "d": 62,
    "d#": 63,
    "eb": 63,
    "e": 64,
    "f": 65,
    "f#": 66,
    "gb": 66,
    "g": 67,
    "g#": 68,
    "ab": 68,
    "a": 69,
    "a#": 70,
    "hb": 70,
    "h": 71,
}


def get_note_num_from_name(name: str) -> int:
    reg_result = regexp.match(name)
    if reg_result is None:
        raise ValueError(f"Unknown note: {name}")
    dict_ = reg_result.groupdict()

    symbol = dict_["symbol"].lower()
    note = _notes[symbol]
    note += (int(dict_["octave"]) - 4) * 12
    return note
asdfadf