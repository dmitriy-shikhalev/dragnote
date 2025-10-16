import logging

from dragnote.enums import Choice
from dragnote.getargs import get_args
from dragnote.initialize import initialize
from dragnote.play import play

logging.basicConfig(level=logging.INFO)


def main():
    args = get_args()

    initialize()

    match args.command:
        case Choice.PLAY.value:
            play(args.synth_num)
        case _:
            raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()  # pragma: no cover
