"""ЗО модуля - проигрываение служебных звуков."""

from dragnote.sounds import Sounds, play_sound


def play_ok():
    play_sound(Sounds.DZIN)


def play_before_start():
    play_sound(Sounds.TUK)


def play_mistake():
    play_sound(Sounds.PEEP)


def play_fail():
    play_sound(Sounds.FAIL)


def play_success():
    play_sound(Sounds.OVER)


def play_over():
    play_sound(Sounds.BULK)
