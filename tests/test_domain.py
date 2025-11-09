from fractions import Fraction

import pytest

from dragnote.consts import NAME, OCTAVE, SIGN
from dragnote.domain import Harmony, Note


class TestNote:
    def test_eq_ok(self):
        note_c_sharp = Note(
            name=NAME.C,
            sign=SIGN.SHARP,
            octave=OCTAVE.FIRST,
        )
        note_d_flat = Note(
            name=NAME.D,
            sign=SIGN.FLAT,
            octave=OCTAVE.FIRST,
        )

        assert note_c_sharp == note_d_flat

    def test_eq_error(self):
        note = Note(
            name=NAME.C,
            sign=SIGN.NATURAL,
            octave=OCTAVE.FIRST,
        )

        with pytest.raises(ValueError):
            _ = note == object()

    def test_from_str(self):
        note = Note.from_str("Cbb2")

        assert note == Note(
            name=NAME.C,
            sign=SIGN.DOUBLE_FLAT,
            octave=OCTAVE.SECOND,
        )

    def test_to_note_value(self):
        note = Note(
            name=NAME.C,
            sign=SIGN.NATURAL,
            octave=OCTAVE.FIRST,
        )

        assert note.to_note_value() == 72

    def test_to_str(self):
        note = Note(
            name=NAME.C,
            sign=SIGN.NATURAL,
            octave=OCTAVE.FIRST,
        )

        assert note.to_str() == "C1"


class TestHarmony:
    @staticmethod
    def get_test_harmony():
        return Harmony(
            notes=(
                Note(
                    name=NAME.C,
                    sign=SIGN.NATURAL,
                    octave=OCTAVE.FIRST,
                ),
            ),
            duration=Fraction(3, 4),
        )

    def test_from_str(self):
        harmony = Harmony.from_str("C1", Fraction(3, 4))

        assert harmony == self.get_test_harmony()

    def test_get_duration_in_seconds(self):
        harmony = self.get_test_harmony()

        assert harmony.get_duration_in_seconds(60) == 3

    def test_to_str(self):
        harmony = self.get_test_harmony()

        assert harmony.to_str() == "C1"
