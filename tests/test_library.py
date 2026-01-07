import random
from unittest.mock import Mock, patch

import pytest

from dragnote.errors import NoFile
from dragnote.library import Library


class TestLibrary:
    def test_get_full_list_filename(self):
        result = Library.get_full_list_filename()
        assert result == "compositions/list.yaml"

    @patch("dragnote.library.open")
    def test_get_list_file_descriptor(self, open_mock):
        with patch.object(Library, "get_full_list_filename") as get_full_list_filename_mock:
            result = Library.get_list_file_descriptor()

            get_full_list_filename_mock.assert_called_once_with()
            open_mock.assert_called_once_with(get_full_list_filename_mock.return_value)
            assert result == open_mock.return_value

    @patch("dragnote.library.yaml")
    def test_read_yaml_list_file(self, yaml_mock):
        with patch.object(Library, "get_list_file_descriptor") as get_list_file_descriptor_mock:
            result = Library.read_yaml_list_file()

            get_list_file_descriptor_mock.assert_called_once_with()
            yaml_mock.load.assert_called_once_with(get_list_file_descriptor_mock.return_value, yaml_mock.Loader)
            assert result == yaml_mock.load.return_value

    def test_init(self):
        filenames = [Mock(), Mock(), Mock()]
        with patch.object(
            Library, "read_yaml_list_file", return_value={"compositions": filenames}
        ) as read_yaml_list_file:
            library = Library()

            assert library.filenames == filenames

            read_yaml_list_file.assert_called_once_with()

    def test_check_num(self):
        with patch.object(
            Library, "read_yaml_list_file", return_value={"compositions": ["a", "b", "c"]}
        ) as read_yaml_list_file:
            library = Library()

            for num in range(3):
                library._check_num(num)

            read_yaml_list_file.assert_called_once_with()

    def test_check_num_error(self):
        with patch.object(
            Library, "read_yaml_list_file", return_value={"compositions": ["a", "b", "c"]}
        ) as read_yaml_list_file:
            library = Library()

            with pytest.raises(NoFile):
                library._check_num(3)

            read_yaml_list_file.assert_called_once_with()

    def test_get_filename_ok(self):
        with patch.object(Library, "read_yaml_list_file", return_value={"compositions": ["a", "b", "c"]}):
            library = Library()
            filename = library.get_filename(0)
            assert filename == "a"

    def test_get_filename_error(self):
        with patch.object(Library, "read_yaml_list_file", return_value={"compositions": ["a", "b", "c"]}):
            library = Library()
            with pytest.raises(NoFile):
                library.get_filename(3)

    def test_get_full_filename(self):
        with patch.object(Library, "read_yaml_list_file", return_value={"compositions": ["a", "b", "c"]}):
            library = Library()
            full_filename = library.get_full_filename(0)
            assert full_filename == "compositions/a"

    @patch(
        "dragnote.library.open",
        return_value=Mock(
            __enter__=Mock(),
            __exit__=Mock(),
        ),
    )
    def test_read_composition(self, open_mock):
        num = random.randint(0, 100)

        with (
            patch.object(Library, "read_yaml_list_file", return_value={"compositions": ["a", "b", "c"]}),
            patch.object(Library, "get_full_filename") as get_full_filename_mock,
        ):
            library = Library()
            data = library.read_composition(num)
            assert data == from_str_mock.return_value

            get_full_filename_mock.assert_called_once_with(num)
            open_mock.assert_called_once_with(get_full_filename_mock.return_value)
            open_mock.return_value.__enter__.assert_called_once_with()
            open_mock.return_value.__enter__.return_value.read.assert_called_once_with()
            from_str_mock.assert_called_once_with(open_mock.return_value.__enter__.return_value.read.return_value)
