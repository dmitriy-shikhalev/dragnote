import pytest

from dragnote.library import Library


@pytest.fixture()
def library():
    yield Library()


def test_compositions(library: Library):
    count = len(library.filenames)
    errors = 0
    for i in range(count):
        try:
            library.read_composition(i)
        except Exception as error:
            errors += 1
            print(f"Error: {error}, filename: {library.filenames[i]}")

    if errors:
        raise Exception("Not all compositions are OK", errors)
