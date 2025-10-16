import os

FILENAME = "_current.db"


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
