import logging

from dragnote import database
from dragnote.game import Game
from dragnote.initialize import initialize_midi
from dragnote.parse import parse_composition
from dragnote.sequencer import Sequencer
from dragnote.settings import Settings


logger = logging.getLogger(__name__)


class Main:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.sequencer = Sequencer(settings.synth_num, settings.instrument, settings.volume, settings.tempo)
        initialize_midi()

    def _run_one_game(self):
        composition_num = database.read()
        composition = parse_composition(composition_num)
        game = Game(composition, self.sequencer, self.settings.max_error_count)
        game.play()

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
