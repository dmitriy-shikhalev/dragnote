from fractions import Fraction

from dragnote.consts import NAME, OCTAVE, SIGN
from dragnote.parse import parse_composition_from_txt


def test_parse_composition():
    text = "  C0:H1 (1/2)  Dbb2 (31/65)         \n"
    composition = parse_composition_from_txt(text)

    l_ = list(composition)

    assert len(l_) == 2

    assert len(l_[0].notes) == 2

    assert l_[0].notes[0].name == NAME.C
    assert l_[0].notes[0].sign == SIGN.NATURAL
    assert l_[0].notes[0].octave == OCTAVE.SMALL
    assert l_[0].notes[1].name == NAME.H
    assert l_[0].notes[1].sign == SIGN.NATURAL
    assert l_[0].notes[1].octave == OCTAVE.FIRST

    assert l_[0].duration == Fraction(1, 2)

    assert len(l_[1].notes) == 1

    assert l_[1].notes[0].name == NAME.D
    assert l_[1].notes[0].sign == SIGN.DOUBLE_FLAT
    assert l_[1].notes[0].octave == OCTAVE.SECOND

    assert l_[1].duration == Fraction(31, 65)
