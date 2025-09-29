import argparse
import logging

from dragnote.info import get_synths

logging.basicConfig(level=logging.INFO)


def main():
    """Main function."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        choices=['play', 'synths'],
        dest="command",
    )

    args = parser.parse_args()
    if args.command == "synths":
        get_synths()
    elif args.command == "play":
        raise NotImplementedError
    else:
        raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()