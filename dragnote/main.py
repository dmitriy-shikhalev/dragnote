import logging

from dragnote.initialize import initialize
from dragnote.play import play
from dragnote.settings import Settings


def main():
    settings = Settings()

    logging.basicConfig(level=getattr(logging, settings.log_level))

    initialize()

    play(settings.synth)


if __name__ == "__main__":
    main()  # pragma: no cover
