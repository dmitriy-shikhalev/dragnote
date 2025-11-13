from dragnote.domain import Harmony, Info, Note
from dragnote.sounds import Sounds, play_sound


def read_input(notes_list: list[Note] | Harmony):
    if isinstance(notes_list, list):
        input_str = " ".join(":".join(note.to_str() for note in notes) for notes in notes_list)
    elif isinstance(notes_list, Harmony):
        input_str = notes_list.to_str()
    else:
        raise ValueError(notes_list)
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
