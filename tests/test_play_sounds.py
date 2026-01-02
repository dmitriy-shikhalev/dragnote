from unittest.mock import patch

from dragnote.play_sounds import (
    play_fail,
    play_mistake,
    play_ok,
    play_over,
    play_success,
)
from dragnote.sounds import Sounds


@patch("dragnote.play_sounds.play_sound")
def test_play_ok(play_sound_mock):
    play_ok()

    play_sound_mock.assert_called_once_with(Sounds.DZIN)


@patch("dragnote.play_sounds.play_sound")
def test_play_mistake(play_sound_mock):
    play_mistake()

    play_sound_mock.assert_called_once_with(Sounds.PEEP)


@patch("dragnote.play_sounds.play_sound")
def test_play_fail(play_sound_mock):
    play_fail()

    play_sound_mock.assert_called_once_with(Sounds.FAIL)


@patch("dragnote.play_sounds.play_sound")
def test_play_success(play_sound_mock):
    play_success()

    play_sound_mock.assert_called_once_with(Sounds.OVER)


@patch("dragnote.play_sounds.play_sound")
def test_play_over(play_sound_mock):
    play_over()

    play_sound_mock.assert_called_once_with(Sounds.BULK)
