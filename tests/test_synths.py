from unittest.mock import patch

from dragnote.synths import synths


@patch("dragnote.synths.print")
@patch("dragnote.synths.pygame.midi.get_device_info")
@patch("dragnote.synths.pygame.midi.get_count", return_value=3)
@patch("dragnote.synths.pygame.midi.init")
@patch("dragnote.synths.pygame.init")
def test_synths(init_mock, midi_init_mock, get_count_mock, get_device_info_mock, print_mock):
    synths()

    init_mock.assert_called_once_with()
    midi_init_mock.assert_called_once_with()
    get_count_mock.assert_called_once_with()
    print_mock.assert_any_call("Count of synths is", get_count_mock.return_value)
    assert get_device_info_mock.call_count == 3
    get_device_info_mock.assert_any_call(0)
    get_device_info_mock.assert_any_call(1)
    get_device_info_mock.assert_any_call(2)
    print_mock.assert_any_call(0, get_device_info_mock.return_value)
    print_mock.assert_any_call(1, get_device_info_mock.return_value)
    print_mock.assert_any_call(2, get_device_info_mock.return_value)
