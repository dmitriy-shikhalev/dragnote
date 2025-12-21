"""
Модуль отвечает за взаимодействие с персистентным хранилищем результатов игр.
"""

import os

from dragnote.consts import FILENAME


class Database:
    @staticmethod
    def read() -> int:
        current = 0
        if os.path.exists(FILENAME):
            with open(FILENAME, "r") as fd:
                current = int(fd.read().strip())

        return current

    @staticmethod
    def write(current: int) -> None:
        with open(FILENAME, "w") as fd:
            fd.write(str(current))

    def write_plus_one_to_db(self):
        num = self.read()
        self.write(num + 1)
