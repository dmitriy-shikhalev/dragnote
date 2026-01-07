import pytest

from dragnote.consts import NAME, OCTAVE, SIGN


@pytest.mark.parametrize(
    "en_name, num, error",
    [
        (NAME.C, 60, False),
        (NAME.D, 62, False),
        (NAME.E, 64, False),
        (NAME.F, 65, False),
        (NAME.G, 67, False),
        (NAME.A, 69, False),
        (NAME.H, 71, False),
        (None, None, True),
    ],
)
class TestNANE:
    def test_to_num(self, en_name, num, error):
        if error:
            pytest.skip()
        assert en_name.to_num() == num


@pytest.mark.parametrize(
    "sign, num, error",
    [
        (SIGN.NATURAL, 0, False),
        (SIGN.NATURAL, 0, False),
        (SIGN.FLAT, -1, False),
        (SIGN.DOUBLE_FLAT, -2, False),
        (SIGN.SHARP, 1, False),
        (SIGN.DOUBLE_SHARP, 2, False),
        (None, None, True),
    ],
)
class TestSIGN:
    def test_to_num(self, sign, num, error):
        if error:
            pytest.skip()
        assert sign.to_num() == num


@pytest.mark.parametrize(
    "octave, num, error",
    [
        (OCTAVE.SMALL, 0, False),
        (OCTAVE.FIRST, 1, False),
        (OCTAVE.SECOND, 2, False),
        (None, 3, True),
    ],
)
class TestOCTAVE:
    def test_to_num(self, octave, num, error):
        if error:
            pytest.skip()
        assert octave.to_num() == num
