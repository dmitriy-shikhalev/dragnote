from unittest.mock import patch

from dragnote.initialize import initialize


@patch("dragnote.initialize.pygame.midi.init")
@patch("dragnote.initialize.pygame.mixer.init")
@patch("dragnote.initialize.pygame.init")
def test_initialize(init_mock, mixer_init_mock, midi_init_mock):
    initialize()

    init_mock.assert_called_once_with()
    mixer_init_mock.assert_called_once_with()
    midi_init_mock.assert_called_once_with()
