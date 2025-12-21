import pytest

from dragnote.consts import NAME, OCTAVE, SIGN


@pytest.mark.parametrize(
    "en_name, name, num, error",
    [
        (NAME.C, "C", 60, False),
        (NAME.D, "d", 62, False),
        (NAME.E, "E", 64, False),
        (NAME.F, "f", 65, False),
        (NAME.G, "G", 67, False),
        (NAME.A, "a", 69, False),
        (NAME.H, "H", 71, False),
        (None, "X", None, True),
    ],
)
class TestNANE:
    def test_from_str(self, en_name, name, num, error):
        if not error:
            assert NAME.from_str(name) == en_name
        else:
            with pytest.raises(ValueError):
                NAME.from_str(name)

    def test_to_num(self, en_name, name, num, error):
        if error:
            pytest.skip()
        assert en_name.to_num() == num


@pytest.mark.parametrize(
    "sign, name, num, error",
    [
        (SIGN.NATURAL, "", 0, False),
        (SIGN.NATURAL, None, 0, False),
        (SIGN.FLAT, "b", -1, False),
        (SIGN.DOUBLE_FLAT, "bb", -2, False),
        (SIGN.SHARP, "#", 1, False),
        (SIGN.DOUBLE_SHARP, "##", 2, False),
        (None, "X", None, True),
    ],
)
class TestSIGN:
    def test_from_str(self, sign, name, num, error):
        if not error:
            assert SIGN.from_str(name) == sign
        else:
            with pytest.raises(ValueError):
                _ = SIGN.from_str(name)

    def test_to_num(self, sign, name, num, error):
        if error:
            pytest.skip()
        assert sign.to_num() == num

    def test_to_str(self, sign, name, num, error):
        if error:
            pytest.skip()
        assert sign.to_str() == (name or "")


@pytest.mark.parametrize(
    "octave, name, num, error",
    [
        (OCTAVE.SMALL, "SMALL", 0, False),
        (OCTAVE.FIRST, "FIRST", 1, False),
        (OCTAVE.SECOND, "SECOND", 2, False),
        (None, None, 3, True),
    ],
)
class TestOCTAVE:
    def test_from_num(self, octave, name, num, error):
        if not error:
            assert OCTAVE.from_num(num) == octave
        else:
            with pytest.raises(ValueError):
                _ = OCTAVE.from_num(num)

    def test_to_num(self, octave, name, num, error):
        if error:
            pytest.skip()
        assert octave.to_num() == num
