from unittest.mock import Mock, patch

import pytest

from dragnote.main import main


@patch("dragnote.main.play")
@patch("dragnote.main.print_synths")
@patch("dragnote.main.print_compositions")
@patch("dragnote.main.get_args", return_value=Mock(command="synth"))
def test_main_synth(get_args_mock, print_compositions_mock, print_synths_mock, play_mock):
    main()

    get_args_mock.assert_called_once_with()
    print_synths_mock.assert_called_once_with()
    print_compositions_mock.assert_not_called()
    play_mock.assert_not_called()


@patch("dragnote.main.play")
@patch("dragnote.main.print_synths")
@patch("dragnote.main.print_compositions")
@patch("dragnote.main.get_args", return_value=Mock(command="compositions"))
def test_main_compositions(get_args_mock, print_compositions_mock, print_synths_mock, play_mock):
    main()

    get_args_mock.assert_called_once_with()
    print_synths_mock.assert_not_called()
    print_compositions_mock.assert_called_once_with()
    play_mock.assert_not_called()


@patch("dragnote.main.play")
@patch("dragnote.main.print_synths")
@patch("dragnote.main.print_compositions")
@patch("dragnote.main.get_args", return_value=Mock(command="play"))
def test_main_play(get_args_mock, print_compositions_mock, print_synths_mock, play_mock):
    main()

    get_args_mock.assert_called_once_with()
    print_synths_mock.assert_not_called()
    print_compositions_mock.assert_not_called()
    play_mock.assert_called_once_with(
        get_args_mock.return_value.composition_name,
        get_args_mock.return_value.synth_num,
    )


@patch("dragnote.main.play")
@patch("dragnote.main.print_synths")
@patch("dragnote.main.print_compositions")
@patch("dragnote.main.get_args")
def test_main_error(get_args_mock, print_compositions_mock, print_synths_mock, play_mock):
    with pytest.raises(ValueError):
        main()

    get_args_mock.assert_called_once_with()
    print_synths_mock.assert_not_called()
    print_compositions_mock.assert_not_called()
    play_mock.assert_not_called()
