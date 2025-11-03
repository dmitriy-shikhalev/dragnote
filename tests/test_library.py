from unittest.mock import patch

from dragnote.library import Library


class TestLibrary:
    @patch("dragnote.library.yaml.load")
    def test_init(self, load_mock):
        library = Library()

        load_mock.assert_called_once_with()
        assert library.filenames == ""

