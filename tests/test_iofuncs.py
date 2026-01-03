from unittest.mock import Mock, patch

from dragnote.iofuncs import (
    print_info,
    read_input,
    read_notes,
)


@patch("dragnote.iofuncs.input")
def test_read_input(input_mock):
    result = read_input("C1")

    input_mock.assert_called_once_with("(C1)> ")
    assert result == input_mock.return_value


@patch("dragnote.iofuncs.Composition.from_str")
@patch("dragnote.iofuncs.read_input")
def test_read_notes(read_input_mock, from_str_mock):
    result = read_notes("Test")

    read_input_mock.assert_called_once_with("Test")
    from_str_mock.assert_called_once_with(read_input_mock.return_value)
    assert result == from_str_mock.return_value


@patch("dragnote.iofuncs.print")
def test_print_info(print_mock):
    info = Mock()

    print_info(info)

    print_mock.assert_called_once_with(
        "Current is %s, common count is %s, attempts %s" % (info.current, info.common, info.attempts)
    )
