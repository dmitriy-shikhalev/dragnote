from unittest.mock import Mock, patch

import pytest

from dragnote.errors import GameOver
from dragnote.main import Main, main


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
    @patch("dragnote.main.Database")
    @patch("dragnote.main.Library")
    @patch("dragnote.main.initialize")
    @patch("dragnote.main.Sequencer")
    def test_init(self, sequencer_mock, initialize_mock, library_mock, database_mock):
        settings = Mock()

        main_ = Main(settings)

        assert main_.settings == settings
        sequencer_mock.assert_called_once_with(settings.synth, settings.instrument, settings.volume, settings.tempo)
        assert main_.sequencer == sequencer_mock.return_value
        initialize_mock.assert_called_once_with()
        library_mock.assert_called_once_with()
        assert main_.library == library_mock.return_value
        database_mock.assert_called_once_with()
        assert main_.database == database_mock.return_value

    @patch("dragnote.main.initialize")
    @patch("dragnote.main.Sequencer")
    def test_read_composition(self, sequencer_mock, initialize_mock):
        settings = Mock()
        main_ = Main(settings)
        with (
            patch.object(main_, "database") as database_mock,
            patch.object(main_, "library") as library_mock,
        ):
            result = main_._read_composition()

            database_mock.read.assert_called_once_with()
            library_mock.read_composition.assert_called_once_with(database_mock.read.return_value)

            assert result == library_mock.read_composition.return_value

    @patch("dragnote.main.play_fail")
    @patch("dragnote.main.play_over")
    @patch("dragnote.main.Game")
    @patch("dragnote.main.initialize")
    @patch("dragnote.main.Sequencer")
    def test_run_one_game_ok(self, sequencer_mock, initialize_mock, game_mock, play_over_mock, play_fail_mock):
        settings = Mock()
        main_ = Main(settings)

        with (
            patch.object(main_, "_read_composition") as _read_composition_mock,
            patch.object(main_, "sequencer") as sequencer_mock,
            patch.object(main_, "settings") as settings_mock,
            patch.object(main_.database, "write_plus_one_to_db") as write_plus_one_to_db_mock,
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
            play_over_mock.assert_called_once_with()
            play_fail_mock.assert_not_called()
            write_plus_one_to_db_mock.write_plus_one_to_db()

    @patch("dragnote.main.play_fail")
    @patch("dragnote.main.play_over")
    @patch("dragnote.main.Game", return_value=Mock(play=Mock(side_effect=GameOver)))
    @patch("dragnote.main.initialize")
    @patch("dragnote.main.Sequencer")
    def test_run_one_game_error(self, sequencer_mock, initialize_mock, game_mock, play_over_mock, play_fail_mock):
        settings = Mock()
        main_ = Main(settings)

        with (
            patch.object(main_, "_read_composition") as _read_composition_mock,
            patch.object(main_, "sequencer") as sequencer_mock,
            patch.object(main_, "settings") as settings_mock,
            patch.object(main_.database, "write_plus_one_to_db") as write_plus_one_to_db_mock,
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
            play_over_mock.assert_not_called()
            play_fail_mock.assert_called_once_with()
            write_plus_one_to_db_mock.assert_not_called()

    @patch("dragnote.main.initialize")
    @patch("dragnote.main.Sequencer")
    def test_run(self, sequencer_mock, initialize_mock):
        settings = Mock()
        main_ = Main(settings)

        with patch.object(main_, "_run_one_game", side_effect=ValueError) as run_one_game_mock:
            with pytest.raises(ValueError):
                main_.run()

            run_one_game_mock.assert_called_once_with()
