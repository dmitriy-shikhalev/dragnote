"""ЗО модуля - одна игра. То есть от начала, до ошибки GameOver."""

import logging

from dragnote.database import Database
from dragnote.domain import Composition
from dragnote.initialize import initialize
from dragnote.iofuncs import play_fail, play_over
from dragnote.library import Library
from dragnote.sequencer import Sequencer
from dragnote.settings import Settings

logger = logging.getLogger(__name__)


class Game:
    def __init__(self, settings: Settings):
        self.settings = settings
        initialize()
        self.sequencer = Sequencer(settings.synth, settings.instrument, settings.volume, settings.tempo)
        self.database = Database()
        self.library = Library()

    def _read_composition(self) -> tuple[int, Composition]:
        num = self.database.read()
        composition = self.library.read_composition(num)
        return num, composition

    def _run_one_game(self):
        num, composition = self._read_composition()
        game = Game(
            num, composition, self.sequencer, self.settings.max_error_count, self.settings.volume, self.settings.tempo
        )
        try:
            game.run()
        except GameOver:
            play_fail()
        else:
            self.database.write_plus_one_to_db()

    def run(self):
        while True:
            self._run_one_game()
