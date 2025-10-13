import logging

from dragnote.enums import Choice
from dragnote.getargs import get_args
from dragnote.info import print_compositions, print_synths
from dragnote.play import play

logging.basicConfig(level=logging.INFO)


def main():
    args = get_args()

    if args.command == Choice.COMPOSITIONS.value:
        print_compositions()
    elif args.command == Choice.SYNTH.value:
        print_synths()
    elif args.command == Choice.PLAY.value:
        play(args.composition_name, args.synth_num)
    else:
        raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()  # pragma: no cover
