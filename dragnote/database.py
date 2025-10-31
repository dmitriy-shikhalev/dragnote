import os

import yaml

from dragnote.errors import NoFile

FILENAME = "_current.db"
DIRNAME = "compositions"
LIST_FILENAME = "list.yaml"


def read() -> int:
    if not os.path.exists(FILENAME):
        current = 0
    else:
        with open(FILENAME, "r") as fd:
            current = int(fd.read().strip())

    return current


def write(current: int) -> None:
    with open(FILENAME, "w") as fd:
        fd.write(str(current))


def get_filename(num: int):
    filenames = yaml.load(open(os.path.join(DIRNAME, LIST_FILENAME)), yaml.Loader)["compositions"]
    if num >= len(filenames):
        raise NoFile(f"No composition with num {num}")
    return filenames[num]


def get_full_filename(filename: str) -> str:
    return os.path.join(DIRNAME, filename)
