from unittest.mock import Mock, patch

import pytest

from dragnote.domain import Harmony, Note
from dragnote.iofuncs import (
    print_info,
    read_input,
)


@patch("dragnote.iofuncs.input")
def test_read_input_harmonies_list(input_mock):
    result = read_input(
        harmonies_list=[Harmony(notes=(Note.from_str("C1"),))],
    )

    input_mock.assert_called_once_with("(C1)> ")
    assert result == input_mock.return_value


@patch("dragnote.iofuncs.input")
def test_read_input_first_harmony(input_mock):
    result = read_input(
        first_harmony=Harmony(notes=(Note.from_str("C1"),)),
    )

    input_mock.assert_called_once_with("(First note is C1)> ")
    assert result == input_mock.return_value


@patch("dragnote.iofuncs.input")
def test_read_input_value_error(input_mock):
    with pytest.raises(ValueError):
        _ = read_input()

    input_mock.assert_not_called()


@patch("dragnote.iofuncs.print")
def test_print_info(print_mock):
    info = Mock()

    print_info(info)

    print_mock.assert_called_once_with(
        "Current is %s, common count is %s, attempts %s" % (info.current, info.common, info.attempts)
    )
