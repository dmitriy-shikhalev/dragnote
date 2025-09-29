import argparse
import logging

from dragnote.info import get_synths
from dragnote.lessons import get_lessons

logging.basicConfig(level=logging.INFO)


def main():
    """Main function."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        choices=['study', "lessons", 'synths'],
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
    else:
        raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()