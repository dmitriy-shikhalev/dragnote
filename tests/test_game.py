from unittest.mock import Mock, call, patch

import pytest

from dragnote.errors import GameOver
from dragnote.game import Game


@patch("dragnote.game.Library")
@patch("dragnote.game.Database")
@patch("dragnote.game.Sequencer")
@patch("dragnote.game.initialize")
class TestGame:
    def test_init(self, initialize_mock, sequencer_mock, database_mock, library_mock):
        settings = Mock()
        game = Game(settings)

        assert game.settings == settings
        initialize_mock.assert_called_once_with()
        sequencer_mock.assert_called_once_with(settings.synth, settings.instrument, settings.volume, settings.tempo)
        database_mock.assert_called_once_with()
        library_mock.assert_called_once_with()

        assert game.sequencer == sequencer_mock.return_value
        assert game.database == database_mock.return_value
        assert game.library == library_mock.return_value

    def test_get_composition(self, initialize_mock, sequencer_mock, database_mock, library_mock):
        settings = Mock()
        game = Game(settings)

        composition = game._get_composition()

        game.database.read.assert_called_once_with()
        game.library.read_composition.assert_called_once_with(game.database.read.return_value)
        assert composition == game.library.read_composition.return_value

    @patch("dragnote.game.Exercise")
    def test_run_one_exercise(self, exercise_mock, initialize_mock, sequencer_mock, database_mock, library_mock):
        settings = Mock()
        game = Game(settings)

        with patch.object(game, "_get_composition") as _get_composition_mock:
            game._run_one_exercise()

            _get_composition_mock.assert_called_once_with()
            exercise_mock.assert_called_once_with(_get_composition_mock.return_value, settings.max_error_count)
            exercise_mock.return_value.run.assert_called_once_with()
            game.database.write_plus_one_to_db.assert_called_once_with()

    @patch("dragnote.game.Exercise", return_value=Mock(run=Mock(side_effect=GameOver)))
    def test_run_one_exercise_game_over(
        self, exercise_mock, initialize_mock, sequencer_mock, database_mock, library_mock
    ):
        settings = Mock()
        game = Game(settings)

        with patch.object(game, "_get_composition") as _get_composition_mock:
            game._run_one_exercise()

            _get_composition_mock.assert_called_once_with()
            exercise_mock.assert_called_once_with(_get_composition_mock.return_value, settings.max_error_count)
            exercise_mock.return_value.run.assert_called_once_with()
            game.database.write_plus_one_to_db.assert_not_called()

    def test_run(self, initialize_mock, sequencer_mock, database_mock, library_mock):
        settings = Mock()
        game = Game(settings)

        with patch.object(game, "_run_one_exercise", side_effect=[None, KeyboardInterrupt]) as _run_one_exercise_mock:
            with pytest.raises(KeyboardInterrupt):
                game.run()

            assert _run_one_exercise_mock.call_args_list == [call(), call()]
