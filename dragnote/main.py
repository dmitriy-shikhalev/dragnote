import argparse
import logging

from dragnote.info import get_synths

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
        "--synth-num",
        dest="synth_num",
        type=int,
        required=False,
    )

    args = parser.parse_args()
    if args.command == "study":
        raise NotImplementedError(args)
    elif args.command == "lessons":
        raise NotImplementedError(args)
    elif args.command == "synths":
        get_synths()
    else:
        raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()