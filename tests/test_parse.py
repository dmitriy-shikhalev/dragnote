from fractions import Fraction

from dragnote.consts import NAME, OCTAVE, SIGN
from dragnote.parse import Parser


def test_parser():
    text = "  C0:H1 (1/2)  Dbb2 (31/65)"
    p = Parser(text)

    l = list(p)

    assert len(l) == 2

    assert len(l[0].notes) == 2

    assert l[0].notes[0].name == NAME.C
    assert l[0].notes[0].sign == SIGN.NATURAL
    assert l[0].notes[0].octave == OCTAVE.SMALL
    assert l[0].notes[1].name == NAME.H
    assert l[0].notes[1].sign == SIGN.NATURAL
    assert l[0].notes[1].octave == OCTAVE.FIRST

    assert l[0].duration == Fraction(1, 2)

    assert len(l[1].notes) == 1

    assert l[1].notes[0].name == NAME.D
    assert l[1].notes[0].sign == SIGN.DOUBLE_FLAT
    assert l[1].notes[0].octave == OCTAVE.SECOND

    assert l[1].duration == Fraction(31, 65)
