import argparse
import logging

import pygame.midi

from dragnote.info import get_synths
from dragnote.parse import get_compositions
from dragnote.play import play

logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        choices=["study", "lessons", "synths", "play"],
        dest="command",
    )
    parser.add_argument(
        "--composition-name",
        dest="composition_name",
        type=str,
        required=False,
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
        default=0,
    )
    parser.add_argument(
        "--synth-num",
        dest="synth_num",
        type=int,
        required=False,
    )

    pygame.midi.init()
    args = parser.parse_args()
    if args.command == "study":
        raise NotImplementedError(args)
    elif args.command == "lessons":
        print("Lessons:")
        for lesson in get_compositions():
            print("*", lesson.name)
    elif args.command == "synths":
        get_synths()
    elif args.command == "play":
        play(args.composition_name, args.synth_num, args.instrument_num)
    else:
        raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
