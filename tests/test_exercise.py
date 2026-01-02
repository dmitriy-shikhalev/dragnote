from fractions import Fraction
from unittest.mock import Mock, call, patch

import pytest

from dragnote.consts import NAME, OCTAVE, SIGN
from dragnote.domain import Composition, Harmony, Note
from dragnote.errors import GameOver
from dragnote.exercise import Exercise


class TestExercise:
    @staticmethod
    def get_composition():
        return Composition(
            harmonies=(
                Harmony(notes=(Note(name=NAME.C, sign=SIGN.NATURAL, octave=OCTAVE.FIRST),), duration=Fraction(1 / 2)),
            ),
        )

    def test_init(self):
        composition = self.get_composition()
        exercise = Exercise(composition=composition, max_error_count=3)

        assert exercise.composition == composition
        assert exercise.max_error_count == 3
        assert exercise.current_harmony == 0
        assert exercise.error_count == 0

    def test_get_harmonies(self):
        composition = self.get_composition()
        exercise = Exercise(composition=composition, max_error_count=3)

        assert exercise.get_harmonies() == composition.harmonies

    def test_is_over(self):
        composition = self.get_composition()
        exercise = Exercise(composition=composition, max_error_count=3)

        assert not exercise.is_over()

    def test_is_fail(self):
        composition = self.get_composition()
        exercise = Exercise(composition=composition, max_error_count=3)

        assert not exercise.is_fail()

    @patch("dragnote.exercise.play_mistake")
    @patch("dragnote.exercise.Round", return_value=Mock(run=Mock(return_value=(1, 1))))
    def test_run_one_iterate(self, round_mock, play_mistake_mock):
        composition = self.get_composition()
        exercise = Exercise(composition=composition, max_error_count=3)

        exercise.run_one_iterate()

        round_mock.assert_called_once_with(composition.harmonies)
        round_mock.return_value.run.assert_called_once_with()
        assert exercise.error_count == 1
        play_mistake_mock.assert_called_once_with()
        assert exercise.current_harmony == 1

    @patch("dragnote.exercise.play_success")
    @patch("dragnote.exercise.play_fail")
    @patch("dragnote.exercise.play_before_start")
    def test_run_game_over(self, play_before_start_mock, play_fail_mock, play_success_mock):
        composition = self.get_composition()
        exercise = Exercise(composition=composition, max_error_count=3)

        with (
            patch.object(exercise, "is_over", side_effect=(False, True)) as is_over_mock,
            patch.object(exercise, "run_one_iterate") as run_one_iterate_mock,
            patch.object(exercise, "is_fail", return_value=True) as is_fail_mock,
        ):
            with pytest.raises(GameOver):
                exercise.run()

            play_before_start_mock.assert_called_once_with()
            assert is_over_mock.call_args_list == [call(), call()]
            run_one_iterate_mock.assert_called_once_with()
            is_fail_mock.assert_called_once_with()
            play_fail_mock.assert_called_once_with()
            play_success_mock.assert_not_called()

    @patch("dragnote.exercise.play_success")
    @patch("dragnote.exercise.play_fail")
    @patch("dragnote.exercise.play_before_start")
    def test_run_success(self, play_before_start_mock, play_fail_mock, play_success_mock):
        composition = self.get_composition()
        exercise = Exercise(composition=composition, max_error_count=3)

        with (
            patch.object(exercise, "is_over", side_effect=(False, True)) as is_over_mock,
            patch.object(exercise, "run_one_iterate") as run_one_iterate_mock,
            patch.object(exercise, "is_fail", return_value=False) as is_fail_mock,
        ):
            exercise.run()

            play_before_start_mock.assert_called_once_with()
            assert is_over_mock.call_args_list == [call(), call()]
            run_one_iterate_mock.assert_called_once_with()
            is_fail_mock.assert_called_once_with()
            play_fail_mock.assert_not_called()
            play_success_mock.assert_called_once_with()
