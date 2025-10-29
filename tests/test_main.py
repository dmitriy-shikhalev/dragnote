from unittest.mock import Mock, patch

import pytest

from dragnote.main import main


@patch("dragnote.main.play")
def test_main_synth(play_mock):
    main()

    get_args_mock.assert_called_once_with()
    print_synths_mock.assert_called_once_with()
    print_compositions_mock.assert_not_called()
    play_mock.assert_not_called()


@patch("dragnote.main.play")
def test_main_compositions(play_mock):
    main()

    get_args_mock.assert_called_once_with()
    print_synths_mock.assert_not_called()
    print_compositions_mock.assert_called_once_with()
    play_mock.assert_not_called()


@patch("dragnote.main.play")
def test_main_play(play_mock):
    main()

    get_args_mock.assert_called_once_with()
    print_synths_mock.assert_not_called()
    print_compositions_mock.assert_not_called()
    play_mock.assert_called_once_with(
        get_args_mock.return_value.composition_name,
        get_args_mock.return_value.synth_num,
    )


@patch("dragnote.main.play")
def test_main_error(play_mock):
    with pytest.raises(ValueError):
        main()

    get_args_mock.assert_called_once_with()
    print_synths_mock.assert_not_called()
    print_compositions_mock.assert_not_called()
    play_mock.assert_not_called()
