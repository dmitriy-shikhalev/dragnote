import pytest

from dragnote.notes import get_note_num_from_name


@pytest.mark.parametrize(
    "name, note_num",
    [
        ("C4", 60),
    ],
)
def test_get_note_num_from_name(name, note_num):
    note_ = get_note_num_from_name(name)
    assert note_ == note_num


def test_get_note_num_from_name_error():
    with pytest.raises(ValueError):
        get_note_num_from_name("C")
