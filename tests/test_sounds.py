from unittest.mock import Mock, patch

from dragnote.sounds import play_sound


@patch("dragnote.sounds.pygame.time.Clock")
@patch("dragnote.sounds.pygame.mixer.music")
def test_play_sound(music_mock, clock_mock):
    sound = Mock()
    music_mock.get_busy.side_effect = [True, False]

    play_sound(sound)

    music_mock.load.assert_called_once_with(sound.value)
    music_mock.play.assert_called_once_with()
    assert music_mock.get_busy.call_count == 2
    music_mock.get_busy.assert_any_call()
    clock_mock.assert_called_once_with()
    clock_mock.return_value.tick.assert_called_once_with(10)
