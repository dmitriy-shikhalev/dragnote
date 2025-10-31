from unittest.mock import Mock, patch

import pytest

from dragnote.main import Main, main
from dragnote.sounds import Sounds


@patch("dragnote.main.Main")
@patch(
    "dragnote.main.Settings",
    return_value=Mock(
        log_level="INFO",
    ),
)
def test_main(settings_mock, main_mock):
    main()

    settings_mock.assert_called_once_with()
    main_mock.assert_called_once_with(settings_mock.return_value)
    main_mock.return_value.run.assert_called_once_with()


class TestMain:
    @patch("dragnote.main.initialize_midi")
    @patch("dragnote.main.Sequencer")
    def test_init(self, sequencer_mock, initialize_midi_mock):
        settings = Mock()

        main_ = Main(settings)

        assert main_.settings == settings
        sequencer_mock.assert_called_once_with(settings.synth, settings.instrument, settings.volume, settings.tempo)
        assert main_.sequencer == sequencer_mock.return_value
        initialize_midi_mock.assert_called_once_with()

    @patch("dragnote.main.play_sound")
    @patch("dragnote.main.Game")
    @patch("dragnote.main.initialize_midi")
    @patch("dragnote.main.Sequencer")
    def test_run_one_game(self, sequencer_mock, initialize_midi_mock, game_mock, play_sound_mock):
        settings = Mock()
        main_ = Main(settings)

        with (
            patch.object(main_, "_read_composition") as _read_composition_mock,
            patch.object(main_, "_write_plus_one_to_db") as _write_plus_one_to_db_mock,
            patch.object(main_, "sequencer") as sequencer_mock,
            patch.object(main_, "settings") as settings_mock,
        ):
            main_._run_one_game()

            _read_composition_mock.assert_called_once_with()
            game_mock.assert_called_once_with(
                _read_composition_mock.return_value,
                sequencer_mock,
                settings_mock.max_error_count,
                settings_mock.volume,
                settings_mock.tempo,
            )
            game_mock.return_value.play.assert_called_once_with()
            play_sound_mock.assert_called_once_with(Sounds.OVER)
            _write_plus_one_to_db_mock.assert_called_once_with()

    @patch("dragnote.main.initialize_midi")
    @patch("dragnote.main.Sequencer")
    def test_run(self, sequencer_mock, initialize_midi_mock):
        settings = Mock()
        main_ = Main(settings)

        with patch.object(main_, "_run_one_game", side_effect=ValueError) as run_one_game_mock:
            with pytest.raises(ValueError):
                main_.run()

            run_one_game_mock.assert_called_once_with()
