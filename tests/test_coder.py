import pytest

from dragnote.coder import (
    CompositionCoder,
    DurationCoder,
    HarmonyCoder,
    NameCoder,
    NoteCoder,
    OctaveCoder,
    SignCoder,
)
from dragnote.consts import NAME, OCTAVE, SIGN
from dragnote.domain import Composition, Duration, Harmony, Note
from dragnote.errors import CoderError


class TestOctaveCoder:
    @pytest.mark.parametrize(
        "octave, text",
        [
            (OCTAVE.SMALL, "0"),
            (OCTAVE.FIRST, "1"),
            (OCTAVE.SECOND, "2"),
        ],
    )
    def test_encode(self, octave, text):
        assert OctaveCoder.encode(octave) == text

    def test_encode_error(self):
        with pytest.raises(CoderError):
            _ = OctaveCoder.encode(object())

    @pytest.mark.parametrize(
        "octave, text",
        [
            (OCTAVE.SMALL, "0"),
            (OCTAVE.FIRST, "1"),
            (OCTAVE.SECOND, "2"),
        ],
    )
    def test_decode(self, octave, text):
        assert OctaveCoder.decode(text) == octave

    def test_decode_error(self):
        with pytest.raises(CoderError):
            _ = OctaveCoder.decode("test-error")


class TestSignCoder:
    @pytest.mark.parametrize(
        "sign, text",
        [
            (SIGN.DOUBLE_FLAT, "bb"),
            (SIGN.FLAT, "b"),
            (SIGN.NATURAL, ""),
            (SIGN.SHARP, "#"),
            (SIGN.DOUBLE_SHARP, "##"),
        ],
    )
    def test_encode(self, sign, text):
        assert SignCoder.encode(sign) == text

    def test_encode_error(self):
        with pytest.raises(CoderError):
            _ = SignCoder.encode(object())

    @pytest.mark.parametrize(
        "sign, text",
        [
            (SIGN.DOUBLE_FLAT, "bb"),
            (SIGN.FLAT, "b"),
            (SIGN.NATURAL, ""),
            (SIGN.SHARP, "#"),
            (SIGN.DOUBLE_SHARP, "##"),
        ],
    )
    def test_decode(self, sign, text):
        assert SignCoder.decode(text) == sign

    def test_decode_error(self):
        with pytest.raises(CoderError):
            _ = SignCoder.decode("test-error")


class TestNameCoder:
    @pytest.mark.parametrize(
        "name, text",
        [
            (NAME.C, "C"),
            (NAME.D, "D"),
            (NAME.E, "E"),
            (NAME.F, "F"),
            (NAME.G, "G"),
            (NAME.A, "A"),
            (NAME.H, "H"),
        ],
    )
    def test_encode(self, name, text):
        assert NameCoder.encode(name) == text

    def test_encode_error(self):
        with pytest.raises(CoderError):
            _ = NameCoder.encode(object())

    @pytest.mark.parametrize(
        "name, text",
        [
            (NAME.C, "C"),
            (NAME.D, "D"),
            (NAME.E, "E"),
            (NAME.F, "F"),
            (NAME.G, "G"),
            (NAME.A, "A"),
            (NAME.H, "H"),
        ],
    )
    def test_decode(self, name, text):
        assert NameCoder.decode(text) == name

    def test_decode_error(self):
        with pytest.raises(CoderError):
            _ = NameCoder.decode("test-error")


class TestNoteCoder:
    def test_encode(self):
        note = Note(name=NAME.C, sign=SIGN.DOUBLE_FLAT, octave=OCTAVE.SECOND)
        assert NoteCoder.encode(note) == "Cbb2"

    def test_decode(self):
        note = Note(name=NAME.C, sign=SIGN.DOUBLE_FLAT, octave=OCTAVE.SECOND)
        assert NoteCoder.decode("cbb2") == note


class TestDurationCoder:
    def test_encode(self):
        duration = Duration(numerator=1, denominator=4)
        assert DurationCoder.encode(duration) == "(1/4)"

    def test_decode(self):
        duration = Duration(numerator=1, denominator=4)
        assert DurationCoder.decode("(1/4)") == duration

    def test_decode_error_parenthesis(self):
        with pytest.raises(CoderError):
            _ = DurationCoder.decode("(1/4]")

    def test_decode_error_non_numeric(self):
        with pytest.raises(CoderError):
            _ = DurationCoder.decode("(1/:)")


class TestHarmonyCoder:
    def test_encode_with_duration_false(self):
        harmony = Harmony(
            notes=(
                Note(name=NAME.C, sign=SIGN.NATURAL, octave=OCTAVE.SMALL),
                Note(name=NAME.E, sign=SIGN.FLAT, octave=OCTAVE.FIRST),
                Note(name=NAME.G, sign=SIGN.DOUBLE_SHARP, octave=OCTAVE.SECOND),
            ),
            duration=None,
        )
        assert HarmonyCoder.encode(harmony) == "C0:Eb1:G##2"

    def test_encode_with_duration_true(self):
        harmony = Harmony(
            notes=(
                Note(name=NAME.C, sign=SIGN.NATURAL, octave=OCTAVE.SMALL),
                Note(name=NAME.E, sign=SIGN.FLAT, octave=OCTAVE.FIRST),
                Note(name=NAME.G, sign=SIGN.DOUBLE_SHARP, octave=OCTAVE.SECOND),
            ),
            duration=Duration(numerator=3, denominator=8),
        )
        assert HarmonyCoder.encode(harmony) == "C0:Eb1:G##2(3/8)"

    def test_decode_with_duration_false(self):
        harmony = Harmony(
            notes=(
                Note(name=NAME.C, sign=SIGN.NATURAL, octave=OCTAVE.SMALL),
                Note(name=NAME.E, sign=SIGN.FLAT, octave=OCTAVE.FIRST),
                Note(name=NAME.G, sign=SIGN.DOUBLE_SHARP, octave=OCTAVE.SECOND),
            ),
            duration=Duration(numerator=3, denominator=8),
        )
        assert HarmonyCoder.decode("C0:Eb1:G##2") == harmony

    def test_decode_with_duration_true(self):
        harmony = Harmony(
            notes=(
                Note(name=NAME.C, sign=SIGN.NATURAL, octave=OCTAVE.SMALL),
                Note(name=NAME.E, sign=SIGN.FLAT, octave=OCTAVE.FIRST),
                Note(name=NAME.G, sign=SIGN.DOUBLE_SHARP, octave=OCTAVE.SECOND),
            ),
            duration=Duration(numerator=3, denominator=8),
        )
        assert HarmonyCoder.decode("C0:Eb1:G##2(3/8)") == harmony


class TestCompositionCode:
    def test_encode_with_duration_false(self):
        harmony = Harmony(
            notes=(
                Note(name=NAME.C, sign=SIGN.NATURAL, octave=OCTAVE.SMALL),
                Note(name=NAME.E, sign=SIGN.FLAT, octave=OCTAVE.FIRST),
                Note(name=NAME.G, sign=SIGN.DOUBLE_SHARP, octave=OCTAVE.SECOND),
            ),
            duration=None,
        )
        composition = Composition(
            harmonies=(harmony, harmony, harmony),
        )
        assert CompositionCoder.encode(composition) == "C0:Eb1:G##2 C0:Eb1:G##2 C0:Eb1:G##2"

    def test_encode_with_duration_true(self):
        harmony = Harmony(
            notes=(
                Note(name=NAME.C, sign=SIGN.NATURAL, octave=OCTAVE.SMALL),
                Note(name=NAME.E, sign=SIGN.FLAT, octave=OCTAVE.FIRST),
                Note(name=NAME.G, sign=SIGN.DOUBLE_SHARP, octave=OCTAVE.SECOND),
            ),
            duration=Duration(numerator=3, denominator=8),
        )
        composition = Composition(
            harmonies=(harmony, harmony, harmony),
        )
        assert CompositionCoder.encode(composition) == "C0:Eb1:G##2(3/8) C0:Eb1:G##2(3/8) C0:Eb1:G##2(3/8)"

    def test_decode_with_duration_false(self):
        harmony = Harmony(
            notes=(
                Note(name=NAME.C, sign=SIGN.NATURAL, octave=OCTAVE.SMALL),
                Note(name=NAME.E, sign=SIGN.FLAT, octave=OCTAVE.FIRST),
                Note(name=NAME.G, sign=SIGN.DOUBLE_SHARP, octave=OCTAVE.SECOND),
            ),
            duration=None,
        )
        composition = Composition(
            harmonies=(harmony, harmony, harmony),
        )
        assert CompositionCoder.decode("C0:Eb1:G##2 C0:Eb1:G##2 C0:Eb1:G##2") == composition

    def test_decode_with_duration_true(self):
        harmony = Harmony(
            notes=(
                Note(name=NAME.C, sign=SIGN.NATURAL, octave=OCTAVE.SMALL),
                Note(name=NAME.E, sign=SIGN.FLAT, octave=OCTAVE.FIRST),
                Note(name=NAME.G, sign=SIGN.DOUBLE_SHARP, octave=OCTAVE.SECOND),
            ),
            duration=Duration(numerator=3, denominator=8),
        )
        composition = Composition(
            harmonies=(harmony, harmony, harmony),
        )
        assert CompositionCoder.decode("C0:Eb1:G##2(3/8) \t\nC0:Eb1:G##2(3/8)    C0:Eb1:G##2(3/8)      ") == composition
