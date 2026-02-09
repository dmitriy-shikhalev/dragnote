from unittest.mock import Mock, patch

from dragnote.consts import NAME, OCTAVE, SIGN
from dragnote.domain import Composition, Harmony, Note
from dragnote.round import Round


class TestRound:
    def test_init(self):
        sequencer = Mock()
        harmonies = (Harmony(notes=(Note(name=NAME.C, octave=OCTAVE.FIRST, sign=SIGN.NATURAL),)),)
        round_ = Round(harmonies, greeting="Test", sequencer=sequencer)

        assert round_.harmonies == harmonies
        assert round_.greeting == "Test"
        assert round_.sequencer == sequencer

    @patch(
        "dragnote.round.read_notes",
        return_value=Composition(
            harmonies=(
                Harmony(notes=(Note(name=NAME.C, octave=OCTAVE.FIRST, sign=SIGN.NATURAL),)),
                Harmony(notes=(Note(name=NAME.C, octave=OCTAVE.FIRST, sign=SIGN.NATURAL),)),
            )
        ),
    )
    def test_run(self, read_notes_mock):
        sequencer = Mock()
        harmonies = (
            Harmony(notes=(Note(name=NAME.C, octave=OCTAVE.FIRST, sign=SIGN.NATURAL),)),
            Harmony(notes=(Note(name=NAME.D, octave=OCTAVE.FIRST, sign=SIGN.NATURAL),)),
            Harmony(notes=(Note(name=NAME.E, octave=OCTAVE.FIRST, sign=SIGN.NATURAL),)),
        )
        round_ = Round(harmonies, greeting="Test", sequencer=sequencer)

        count, errors = round_.run()

        assert count == 1
        assert errors == 1
        read_notes_mock.assert_called_once_with("Test")
