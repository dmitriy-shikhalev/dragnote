from dragnote.domain import Info
from dragnote.sounds import Sounds, play_sound


def read_input():
    return input("> ")


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
