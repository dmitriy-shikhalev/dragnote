from fractions import Fraction
from unittest.mock import Mock, patch

import pytest

from dragnote.consts import NAME, OCTAVE, SIGN
from dragnote.parse import (
    parse_composition,
    parse_duration,
    parse_notes,
    read_composition,
)


@patch("dragnote.parse.Note")
def test_parse_notes(note_mock):
    notes_str = "a:b:c"
    result = parse_notes(notes_str)

    note1 = next(result)
    note2 = next(result)
    note3 = next(result)

    with pytest.raises(StopIteration):
        next(result)

    assert note_mock.from_str.call_count == 3

    note_mock.from_str.assert_any_call("a")
    note_mock.from_str.assert_any_call("b")
    note_mock.from_str.assert_any_call("c")

    assert note1 == note2 == note3 == note_mock.from_str.return_value


def test_parse_duration_ok():
    duration_str = "(1/2)"
    duration = parse_duration(duration_str)
    assert duration == Fraction(1, 2)


def test_parse_duration_error():
    duration_str = "(1/2"
    with pytest.raises(ValueError):
        _ = parse_duration(duration_str)


@patch("dragnote.parse.parse_composition")
@patch(
    "dragnote.parse.open",
    return_value=Mock(
        __enter__=Mock(),
        __exit__=Mock(),
    ),
)
@patch("dragnote.parse.get_full_filename")
@patch("dragnote.parse.get_filename")
def test_read_composition(get_filename_mock, get_full_filename_mock, open_mock, parse_composition_mock):
    num = Mock()
    result = read_composition(num)

    assert result == parse_composition_mock.return_value

    get_filename_mock.assert_called_once_with(num)
    get_full_filename_mock.assert_called_once_with(get_filename_mock.return_value)
    open_mock.assert_called_once_with(get_full_filename_mock.return_value)
    parse_composition_mock.assert_called_once_with(open_mock.return_value.__enter__.return_value.read.return_value)


def test_parse_composition_ok():
    text = "  C0:H1 (1/2)  Dbb2 (31/65)         \n"
    composition = parse_composition(text)

    l_ = list(composition)

    assert len(l_) == 2

    assert len(l_[0].notes) == 2

    assert l_[0].notes[0].name == NAME.C
    assert l_[0].notes[0].sign == SIGN.NATURAL
    assert l_[0].notes[0].octave == OCTAVE.SMALL
    assert l_[0].notes[1].name == NAME.H
    assert l_[0].notes[1].sign == SIGN.NATURAL
    assert l_[0].notes[1].octave == OCTAVE.FIRST

    assert l_[0].duration == Fraction(1, 2)

    assert len(l_[1].notes) == 1

    assert l_[1].notes[0].name == NAME.D
    assert l_[1].notes[0].sign == SIGN.DOUBLE_FLAT
    assert l_[1].notes[0].octave == OCTAVE.SECOND

    assert l_[1].duration == Fraction(31, 65)
