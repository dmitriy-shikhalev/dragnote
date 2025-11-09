from unittest.mock import Mock, patch

import pytest

from dragnote.errors import EmptyInput, GameOver
from dragnote.game import Game


class TestGame:
    @staticmethod
    def get_game():
        composition = Mock()
        sequencer = Mock()
        max_error_count = Mock()
        volume = Mock()
        tempo = Mock()
        _init_queue = Mock()

        with patch.object(Game, "_init_queue"):
            return Game(composition, sequencer, max_error_count, volume, tempo)

    @patch("dragnote.game.Queue")
    @patch("dragnote.game.InputQueue")
    def test_init(self, input_queue_mock, queue_mock):
        composition = Mock()
        sequencer = Mock()
        max_error_count = Mock()
        volume = Mock()
        tempo = Mock()

        with patch.object(Game, "_init_queue") as _init_queue_mock:
            game = Game(composition, sequencer, max_error_count, volume, tempo)

            input_queue_mock.assert_called_once_with()
            assert game.composition == composition
            assert game.sequencer == sequencer
            assert game.max_error_count == max_error_count
            assert game.volume == volume
            assert game.tempo == tempo
            assert game.input_queue == input_queue_mock.return_value
            assert game.error_count == 0
            queue_mock.assert_called_once_with()
            assert game.queue == queue_mock.return_value
            _init_queue_mock.assert_called_once_with()

    def test_play_composition(self):
        game = self.get_game()

        with patch.object(game.sequencer, "play_composition") as play_composition_mock:
            game._play_composition()

            play_composition_mock.assert_called_once_with(game.composition)

    def test_init_queue(self):
        composition = [Mock()]
        sequencer = Mock()
        max_error_count = Mock()
        volume = Mock()
        tempo = Mock()

        game = Game(composition, sequencer, max_error_count, volume, tempo)

        with patch.object(game, "queue") as queue_mock:
            game._init_queue()

            queue_mock.put.assert_called_once_with(composition[0])

    @patch("dragnote.game.play_ok")
    def test_ok(self, play_ok_mock):
        harmony = Mock()
        game = self.get_game()

        game._ok(harmony)

        play_ok_mock.assert_called_once_with()
        game.sequencer.play_harmony.assert_called_once_with(harmony)
        assert game.error_count == 0

    @patch("dragnote.game.tuple")
    @patch("dragnote.game.Harmony")
    @patch("dragnote.game.play_mistake")
    def test_mistake_not_game_over(self, play_mistake_mock, harmony_mock, tuple_mock):
        harmony = Mock()
        notes = [Mock()]
        game = self.get_game()
        game.error_count = 123
        game.max_error_count = 124

        with (
            patch.object(game.queue, "put") as put_mock,
            patch.object(game.sequencer, "play_harmony") as play_harmony_mock,
        ):
            game._mistake(harmony, notes)

            put_mock.assert_called_once_with(harmony)
            play_mistake_mock.assert_called_once_with()
            assert play_harmony_mock.call_count == 2
            play_harmony_mock.assert_any_call(harmony)
            tuple_mock.assert_called_once_with(notes)
            harmony_mock.assert_called_once_with(notes=tuple_mock.return_value, duration=harmony.duration)
            play_harmony_mock.assert_any_call(harmony_mock.return_value)
            assert game.error_count == 124

    @patch("dragnote.game.tuple")
    @patch("dragnote.game.Harmony")
    @patch("dragnote.game.play_mistake")
    def test_mistake_game_over(self, play_mistake_mock, harmony_mock, tuple_mock):
        harmony = Mock()
        notes = [Mock()]
        game = self.get_game()
        game.error_count = 123
        game.max_error_count = 123

        with (
            patch.object(game.queue, "put") as put_mock,
            patch.object(game.sequencer, "play_harmony") as play_harmony_mock,
        ):
            with pytest.raises(GameOver):
                game._mistake(harmony, notes)

            put_mock.assert_called_once_with(harmony)
            play_mistake_mock.assert_called_once_with()
            assert play_harmony_mock.call_count == 2
            play_harmony_mock.assert_any_call(harmony)
            tuple_mock.assert_called_once_with(notes)
            harmony_mock.assert_called_once_with(notes=tuple_mock.return_value, duration=harmony.duration)
            play_harmony_mock.assert_any_call(harmony_mock.return_value)
            assert game.error_count == 124

    @patch("dragnote.game.read_input")
    def test_read_input_ok(self, read_input_mock):
        game = self.get_game()
        result = game._read_input()

        read_input_mock.assert_called_once_with()
        assert result == read_input_mock.return_value

    @patch("dragnote.game.read_input", return_value="")
    def test_read_input_error(self, read_input_mock):
        game = self.get_game()

        with pytest.raises(EmptyInput):
            _ = game._read_input()

        read_input_mock.assert_called_once_with()

    @patch("dragnote.game.parse_notes")
    def test_get_notes(self, parse_notes_mock):
        game = self.get_game()

        with patch.object(game, "_read_input") as _read_input_mock:
            result = game._get_notes()

            _read_input_mock.assert_called_once_with()
            parse_notes_mock.assert_called_once_with(_read_input_mock.return_value)
            assert result == parse_notes_mock.return_value

    @patch("dragnote.game.set")
    def test_is_harmony_eq_notes_eq(self, set_mock):
        game = self.get_game()
        harmony = Mock()
        notes = [Mock()]

        assert game._is_harmony_eq_notes(harmony, notes)
        assert set_mock.call_count == 2
        set_mock.assert_any_call(harmony.notes)
        set_mock.assert_any_call(notes)

    @patch("dragnote.game.set", side_effect=["a", "b"])
    def test_is_harmony_eq_notes_neq(self, set_mock):
        game = self.get_game()
        harmony = Mock()
        notes = [Mock()]

        assert not game._is_harmony_eq_notes(harmony, notes)
        assert set_mock.call_count == 2
        set_mock.assert_any_call(harmony.notes)
        set_mock.assert_any_call(notes)

    def test_one_iterate_play_empty_input(self):
        game = self.get_game()

        with (
            patch.object(game, "_get_notes", side_effect=EmptyInput) as _get_notes_mock,
            patch.object(game, "_play_composition") as _play_composition_mock,
            patch.object(game.queue, "get") as get_mock,
            patch.object(game, "_is_harmony_eq_notes") as _is_harmony_eq_notes_mock,
            patch.object(game, "_ok") as _ok_mock,
            patch.object(game, "_mistake") as _mistake_mock,
        ):
            game._one_iterate_play()

            _get_notes_mock.assert_called_once_with()
            _play_composition_mock.assert_called_once_with()
            get_mock.assert_not_called()
            _is_harmony_eq_notes_mock.assert_not_called()
            _ok_mock.assert_not_called()
            _mistake_mock.assert_not_called()

    def test_one_iterate_play_ok(self):
        game = self.get_game()

        with (
            patch.object(game, "_get_notes") as _get_notes_mock,
            patch.object(game, "_play_composition") as _play_composition_mock,
            patch.object(game.queue, "get") as get_mock,
            patch.object(game, "_is_harmony_eq_notes", return_value=True) as _is_harmony_eq_notes_mock,
            patch.object(game, "_ok") as _ok_mock,
            patch.object(game, "_mistake") as _mistake_mock,
        ):
            game._one_iterate_play()

            _get_notes_mock.assert_called_once_with()
            _play_composition_mock.assert_not_called()
            get_mock.assert_called_once_with()
            _is_harmony_eq_notes_mock.assert_called_once_with(get_mock.return_value, _get_notes_mock.return_value)
            _ok_mock.assert_called_once_with(get_mock.return_value)
            _mistake_mock.assert_not_called()

    def test_one_iterate_play_mistake(self):
        game = self.get_game()

        with (
            patch.object(game, "_get_notes") as _get_notes_mock,
            patch.object(game, "_play_composition") as _play_composition_mock,
            patch.object(game.queue, "get") as get_mock,
            patch.object(game, "_is_harmony_eq_notes", return_value=False) as _is_harmony_eq_notes_mock,
            patch.object(game, "_ok") as _ok_mock,
            patch.object(game, "_mistake") as _mistake_mock,
        ):
            game._one_iterate_play()

            _get_notes_mock.assert_called_once_with()
            _play_composition_mock.assert_not_called()
            get_mock.assert_called_once_with()
            _is_harmony_eq_notes_mock.assert_called_once_with(get_mock.return_value, _get_notes_mock.return_value)
            _ok_mock.aassert_not_called()
            _mistake_mock.assert_called_once_with(get_mock.return_value, _get_notes_mock.return_value)

    @patch("dragnote.game.play_over")
    def test_play(self, play_over_mock):
        game = self.get_game()

        with (
            patch.object(game, "_play_composition") as _play_composition_mock,
            patch.object(game.queue, "qsize") as qsize_mock,
            patch.object(game, "_one_iterate_play") as _one_iterate_play_mock,
        ):
            game.queue.qsize.side_effect = [1, 0]

            game.play()

            _play_composition_mock.assert_called_once_with()
            assert qsize_mock.call_count == 2
            qsize_mock.assert_any_call()
            _one_iterate_play_mock.assert_called_once_with()
            play_over_mock.assert_called_once_with()
