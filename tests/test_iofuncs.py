from unittest.mock import Mock, patch

from dragnote.domain import Harmony, Note
from dragnote.iofuncs import (
    play_fail,
    play_mistake,
    play_ok,
    play_over,
    play_success,
    print_info,
    read_input,
)
from dragnote.sounds import Sounds


@patch("dragnote.iofuncs.input")
def test_read_input(input_mock):
    result = read_input(
        first_harmony=Harmony(notes=(Note.from_str("C1"),)),
    )

    input_mock.assert_called_once_with("(First note is C1)> ")
    assert result == input_mock.return_value


@patch("dragnote.iofuncs.print")
def test_print_info(print_mock):
    info = Mock()

    print_info(info)

    print_mock.assert_called_once_with(
        "Current is %s, common count is %s, attempts %s" % (info.current, info.common, info.attempts)
    )


@patch("dragnote.iofuncs.play_sound")
def test_play_ok(play_sound_mock):
    play_ok()

    play_sound_mock.assert_called_once_with(Sounds.DZIN)


@patch("dragnote.iofuncs.play_sound")
def test_play_mistake(play_sound_mock):
    play_mistake()

    play_sound_mock.assert_called_once_with(Sounds.PEEP)


@patch("dragnote.iofuncs.play_sound")
def test_play_fail(play_sound_mock):
    play_fail()

    play_sound_mock.assert_called_once_with(Sounds.FAIL)


@patch("dragnote.iofuncs.play_sound")
def test_play_success(play_sound_mock):
    play_success()

    play_sound_mock.assert_called_once_with(Sounds.OVER)


@patch("dragnote.iofuncs.play_sound")
def test_play_over(play_sound_mock):
    play_over()

    play_sound_mock.assert_called_once_with(Sounds.BULK)
