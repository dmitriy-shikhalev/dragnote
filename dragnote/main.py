import logging

from dragnote import database
from dragnote.domain import Composition
from dragnote.game import Game
from dragnote.initialize import initialize_midi
from dragnote.parse import parse_composition_from_num
from dragnote.sequencer import Sequencer
from dragnote.settings import Settings
from dragnote.sounds import Sounds, play_sound

logger = logging.getLogger(__name__)


class Main:
    def __init__(self, settings: Settings):
        self.settings = settings
        initialize_midi()
        self.sequencer = Sequencer(settings.synth, settings.instrument, settings.volume, settings.tempo)

    @staticmethod
    def _read_composition() -> Composition:
        num = database.read()
        composition = parse_composition_from_num(num)
        return composition

    @staticmethod
    def _write_plus_one_to_db():
        num = database.read()
        database.write(num + 1)

    def _run_one_game(self):
        composition = self._read_composition()
        game = Game(
            composition, self.sequencer, self.settings.max_error_count, self.settings.volume, self.settings.tempo
        )
        try:
            game.play()
        except ValueError:
            play_sound(Sounds.BULK)
        else:
            play_sound(Sounds.OVER)
            self._write_plus_one_to_db()

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
