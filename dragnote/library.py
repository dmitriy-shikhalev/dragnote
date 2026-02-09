"""ЗО модуля - чтение библиотеки упражнений."""

import os

import yaml

from dragnote.coder import CompositionCoder
from dragnote.consts import DIRNAME, LIST_FILENAME
from dragnote.domain import Composition
from dragnote.errors import NoFile


class Library:
    @staticmethod
    def get_full_list_filename():
        return os.path.join(DIRNAME, LIST_FILENAME)

    @classmethod
    def get_list_file_descriptor(cls):
        return open(cls.get_full_list_filename())

    @classmethod
    def read_yaml_list_file(cls):
        return yaml.load(cls.get_list_file_descriptor(), yaml.Loader)

    def __init__(self):
        self.filenames = self.read_yaml_list_file()["compositions"]

    @property
    def count(self):
        return len(self.filenames)

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

        return CompositionCoder.decode(txt)
