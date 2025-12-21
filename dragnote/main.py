"""
ЗО модуля - обеспечить точку входа в программу из терминала.
"""

import logging

from dragnote.game import Game
from dragnote.settings import Settings


def main():
    settings = Settings()

    logging.basicConfig(level=getattr(logging, settings.log_level))

    game_instance = Game(settings)
    game_instance.run()


if __name__ == "__main__":
    main()  # pragma: no cover
