from fractions import Fraction

import pytest

from dragnote.consts import NAME, OCTAVE, SIGN
from dragnote.domain import Composition, Harmony, Note


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
        harmony = Harmony.from_str("C1(3/4)")

        assert harmony == self.get_test_harmony()

    def test_from_str_with_duration(self):
        harmony = Harmony.from_str("C1", duration=Fraction(3, 4))

        assert harmony == self.get_test_harmony()

    def test_from_str_error(self):
        with pytest.raises(ValueError):
            _ = Harmony.from_str("C1(3/4)asdf")

    def test_get_duration_in_seconds(self):
        harmony = self.get_test_harmony()

        assert harmony.get_duration_in_seconds(60) == 3

    def test_get_duration_in_seconds_without_duration(self):
        harmony = Harmony(notes=self.get_test_harmony().notes, duration=None)

        with pytest.raises(ValueError):
            _ = harmony.get_duration_in_seconds(80)

    def test_to_str(self):
        harmony = self.get_test_harmony()

        assert harmony.to_str() == "C1"

    def test_eq_raise_value_error(self):
        harmony = self.get_test_harmony()

        with pytest.raises(ValueError):
            _ = harmony == "abc"

    def test_eq_true(self):
        harmony = self.get_test_harmony()

        assert harmony == harmony

    def test_eq_true_without_duration(self):
        harmony = self.get_test_harmony()
        harmony_without_duration = Harmony(notes=harmony.notes)

        assert harmony == harmony_without_duration

    def test_eq_false(self):
        harmony = self.get_test_harmony()
        empty_harmony = Harmony(notes=())
        assert not harmony == empty_harmony


class TestComposition:
    def test_from_str(self):
        temp_string = "A1(1/2)  \t\n Cbb1(3/45)"
        composition = Composition.from_str(temp_string)

        assert len(composition.harmonies) == 2
        assert composition.harmonies[0] == Harmony(
            notes=(Note(NAME.A, sign=SIGN.NATURAL, octave=OCTAVE.FIRST),), duration=Fraction(1, 2)
        )
        assert composition.harmonies[1] == Harmony(
            notes=(Note(NAME.C, sign=SIGN.DOUBLE_FLAT, octave=OCTAVE.FIRST),), duration=Fraction(3, 45)
        )
