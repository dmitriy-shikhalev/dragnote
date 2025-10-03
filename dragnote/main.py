import argparse
import logging
from fractions import Fraction

from dragnote.domain import Event, Klass, Name, Note, Sign, Schedule, Harmony, Voice, Composition
from dragnote.info import get_synths
from dragnote.lessons import get_lessons
from dragnote.sequencer import Sequencer

logging.basicConfig(level=logging.DEBUG)


def test(synth_num):  # todo: remove
    import pygame.midi
    pygame.midi.init()
    sequencer = Sequencer(synth_num)
    sequencer.play_composition(
        Composition(
            voices=(
                Voice(
                    harmonies=(
                        Harmony(
                            notes=(
                                Note(
                                    name=Name.C,
                                    sign=Sign.NATURAL,
                                    octave=3,
                                    duration=Fraction(1, 4),
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 4)
                        ),
                        Harmony(
                            notes=(
                                Note(
                                    name=Name.E,
                                    sign=Sign.NATURAL,
                                    octave=3,
                                    duration=Fraction(1, 4),
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 4)
                        ),
                        Harmony(
                            notes=(
                                Note(
                                    name=Name.G,
                                    sign=Sign.NATURAL,
                                    octave=3,
                                    duration=Fraction(1, 4),
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 4)
                        ),
                        Harmony(
                            notes=(
                                Note(
                                    name=Name.C,
                                    sign=Sign.NATURAL,
                                    octave=4,
                                    duration=Fraction(1, 4),
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 4)
                        ),
                        Harmony(
                            notes=(
                                Note(
                                    name=Name.G,
                                    sign=Sign.NATURAL,
                                    octave=3,
                                    duration=Fraction(1, 4),
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 4)
                        ),
                        Harmony(
                            notes=(
                                Note(
                                    name=Name.E,
                                    sign=Sign.NATURAL,
                                    octave=3,
                                    duration=Fraction(1, 4),
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 4)
                        ),
                        Harmony(
                            notes=(
                                Note(
                                    name=Name.C,
                                    sign=Sign.NATURAL,
                                    octave=3,
                                    duration=Fraction(1, 4),
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 4)
                        ),

                        Harmony(
                            notes=(
                                Note(
                                    name=Name.P,
                                    sign=Sign.NATURAL,
                                    octave=3,
                                    duration=Fraction(1, 4),
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 4)
                        ),

                        Harmony(
                            notes=(
                                Note(
                                    name=Name.C,
                                    sign=Sign.NATURAL,
                                    octave=3,
                                    duration=Fraction(1, 2),
                                    volume=100,
                                ),
                                Note(
                                    name=Name.E,
                                    sign=Sign.NATURAL,
                                    octave=3,
                                    duration=Fraction(1, 2),
                                    volume=100,
                                ),
                                Note(
                                    name=Name.G,
                                    sign=Sign.NATURAL,
                                    octave=3,
                                    duration=Fraction(1, 2),
                                    volume=100,
                                ),
                            ),
                            duration=Fraction(1, 2)
                        ),
                    )
                ),
            ),
            tempo=100,
            tonality="C-dur",
            name="asdf",
        ),
    )

def main():
    """Main function."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        choices=['study', "lessons", 'synths', "test"],
        dest="command",
    )
    parser.add_argument(
        "--lesson-num",
        dest="lesson_num",
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
        test(args.synth_num)
    else:
        raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()