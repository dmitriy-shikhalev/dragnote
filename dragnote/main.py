import logging

from dragnote.database import Database
from dragnote.domain import Composition
from dragnote.errors import GameOver
from dragnote.game import Game
from dragnote.initialize import initialize
from dragnote.iofuncs import play_fail, play_over
from dragnote.library import Library
from dragnote.sequencer import Sequencer
from dragnote.settings import Settings

logger = logging.getLogger(__name__)


class Main:
    def __init__(self, settings: Settings):
        self.settings = settings
        initialize()
        self.sequencer = Sequencer(settings.synth, settings.instrument, settings.volume, settings.tempo)
        self.database = Database()
        self.library = Library()

    def _read_composition(self) -> Composition:
        num = self.database.read()
        composition = self.library.read_composition(num)
        return composition

    def _run_one_game(self):
        composition = self._read_composition()
        game = Game(
            composition, self.sequencer, self.settings.max_error_count, self.settings.volume, self.settings.tempo
        )
        try:
            game.play()
        except GameOver:
            play_fail()
        else:
            play_over()
            self.database.write_plus_one_to_db()

    def run(self):
        while True:
            self._run_one_game()


def main():
    settings = Settings()

    logging.basicConfig(level=getattr(logging, settings.log_level))

    main_instance = Main(settings)
    main_instance.run()


if __name__ == "__main__":
    main()  # pragma: no cover
