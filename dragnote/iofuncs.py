from dragnote.domain import Harmony, Info, Note
from dragnote.sounds import Sounds, play_sound


def read_input(notes_list: list[Note] = None, first_note: Harmony = None):
    if notes_list:
        input_str = " ".join(":".join(note.to_str() for note in notes) for notes in notes_list)
    elif first_note:
        input_str = f"First note is {first_note.to_str()}"
    else:
        raise ValueError("Notes list is None and first_note is None")
    return input(f"({input_str})> ")


def print_info(info: Info):
    print("Current is %s, common count is %s, attempts %s" % (info.current, info.common, info.attempts))


def play_ok():
    play_sound(Sounds.DZIN)


def play_mistake():
    play_sound(Sounds.PEEP)


def play_fail():
    play_sound(Sounds.FAIL)


def play_success():
    play_sound(Sounds.OVER)


def play_over():
    play_sound(Sounds.BULK)
