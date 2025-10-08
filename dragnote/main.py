import argparse
import logging
from fractions import Fraction

import pygame.midi

from dragnote.consts import NAME, OCTAVE, SIGN
from dragnote.domain import Composition, Harmony, Note, Voice
from dragnote.info import get_synths
from dragnote.lessons import get_lessons
from dragnote.sequencer import Sequencer

logging.basicConfig(level=logging.DEBUG)


def play_test_composition(sequencer: Sequencer):
    sequencer.play_composition(
        Composition(
            voices=(
                Voice(
                    harmonies=(
                        Harmony(
                            notes=(
                                Note(
                                    name=NAME.C,
                                    sign=SIGN.NATURAL,
                                    octave=OCTAVE.FIRST,
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 4),
                        ),
                        Harmony(
                            notes=(
                                Note(
                                    name=NAME.E,
                                    sign=SIGN.NATURAL,
                                    octave=OCTAVE.FIRST,
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 4),
                        ),
                        Harmony(
                            notes=(
                                Note(
                                    name=NAME.G,
                                    sign=SIGN.NATURAL,
                                    octave=OCTAVE.FIRST,
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 4),
                        ),
                        Harmony(
                            notes=(
                                Note(
                                    name=NAME.C,
                                    sign=SIGN.NATURAL,
                                    octave=OCTAVE.SECOND,
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 4),
                        ),
                        Harmony(
                            notes=(
                                Note(
                                    name=NAME.G,
                                    sign=SIGN.NATURAL,
                                    octave=OCTAVE.FIRST,
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 4),
                        ),
                        Harmony(
                            notes=(
                                Note(
                                    name=NAME.E,
                                    sign=SIGN.NATURAL,
                                    octave=OCTAVE.FIRST,
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 4),
                        ),
                        Harmony(
                            notes=(
                                Note(
                                    name=NAME.C,
                                    sign=SIGN.NATURAL,
                                    octave=OCTAVE.FIRST,
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 4),
                        ),
                        Harmony(
                            notes=(
                                Note(
                                    name=NAME.P,
                                    sign=SIGN.NATURAL,
                                    octave=OCTAVE.FIRST,
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 4),
                        ),
                        Harmony(
                            notes=(
                                Note(
                                    name=NAME.C,
                                    sign=SIGN.NATURAL,
                                    octave=OCTAVE.FIRST,
                                    volume=100,
                                ),
                                Note(
                                    name=NAME.E,
                                    sign=SIGN.NATURAL,
                                    octave=OCTAVE.FIRST,
                                    volume=100,
                                ),
                                Note(
                                    name=NAME.G,
                                    sign=SIGN.NATURAL,
                                    octave=OCTAVE.FIRST,
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 2),
                        ),
                    )
                ),
            ),
            tempo=100,
            tonality="C-dur",
            name="asdf",
        ),
    )


def test(synth_num, instrument_num):  # todo: remove
    pygame.midi.init()
    sequencer = Sequencer(synth_num, instrument_num)
    # play_test_note(sequencer)
    play_test_composition(sequencer)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        choices=["study", "lessons", "synths", "test"],
        dest="command",
    )
    parser.add_argument(
        "--lesson-num",
        dest="lesson_num",
        type=int,
        required=False,
    )
    parser.add_argument(
        "--instrument-num",
        dest="instrument_num",
        type=int,
        required=False,
    )
    parser.add_argument(
        "--lessons-path",
        dest="lessons_path",
        type=str,
        required=False,
        default="lessons",
    )
    parser.add_argument(
        "--synth-num",
        dest="synth_num",
        type=int,
        required=False,
    )

    args = parser.parse_args()
    if args.command == "study":
        raise NotImplementedError(args)
    elif args.command == "lessons":
        print("Lessons:")
        for lesson in get_lessons(args.lessons_path):
            print(lesson)
    elif args.command == "synths":
        get_synths()
    elif args.command == "test":
        test(args.synth_num, args.instrument_num)
    else:
        raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
