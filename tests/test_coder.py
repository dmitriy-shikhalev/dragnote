import pytest

from dragnote.coder import NameCoder, OctaveCoder, SignCoder
from dragnote.domain import NAME, OCTAVE, SIGN


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
        with pytest.raises(ValueError):
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
        with pytest.raises(ValueError):
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
        with pytest.raises(ValueError):
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
        with pytest.raises(ValueError):
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
        with pytest.raises(ValueError):
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
        with pytest.raises(ValueError):
            _ = NameCoder.decode("test-error")
