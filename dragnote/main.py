import logging

from dragnote.initialize import initialize
from dragnote.play import play
from dragnote.settings import Settings

logging.basicConfig(level=logging.INFO)


def main():
    settings = Settings()

    initialize()

    play(settings.synth)


if __name__ == "__main__":
    main()  # pragma: no cover
