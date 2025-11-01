import os

import yaml

from dragnote.consts import DIRNAME, LIST_FILENAME
from dragnote.domain import Composition
from dragnote.errors import NoFile
from dragnote.parse import parse_composition


class Library:
    def __init__(self):
        self.filenames = yaml.load(open(os.path.join(DIRNAME, LIST_FILENAME)), yaml.Loader)["compositions"]

    def _check_num(self, num):
        if num >= len(self.filenames):
            raise NoFile(f"No composition with num {num}")

    def get_filename(self, num: int) -> str:
        self._check_num(num)
        return self.filenames[num]

    def get_full_filename(self, num: int) -> str:
        return os.path.join(DIRNAME, self.get_filename(num))

    def read_composition(self, num: int) -> Composition:
        with open(self.get_full_filename(num)) as fd:
            txt = fd.read()

        return parse_composition(txt)
