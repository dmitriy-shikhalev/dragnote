from unittest.mock import Mock, patch

from dragnote.consts import FILENAME
from dragnote.database import Database


class TestDatabase:
    @patch("dragnote.database.open")
    @patch("dragnote.database.os.path.exists", return_value=False)
    def test_read_not_exists(self, exists_mock, open_mock):
        value = Database.read()

        assert value == 0
        exists_mock.assert_called_once_with(FILENAME)
        open_mock.assert_not_called()

    @patch(
        "dragnote.database.open",
        return_value=Mock(
            __enter__=Mock(return_value=Mock(read=Mock(return_value=" 123 "))),
            __exit__=Mock(),
        ),
    )
    @patch("dragnote.database.os.path.exists", return_value=True)
    def test_read_exists(self, exists_mock, open_mock):
        value = Database.read()

        assert value == 123
        exists_mock.assert_called_once_with(FILENAME)
        open_mock.assert_called_once_with(FILENAME, "r")

    @patch(
        "dragnote.database.open",
        return_value=Mock(
            __enter__=Mock(return_value=Mock(write=Mock())),
            __exit__=Mock(),
        ),
    )
    def test_write(self, open_mock):
        Database.write(123)

        open_mock.assert_called_once_with(FILENAME, "w")
        open_mock.return_value.__enter__.return_value.write.assert_called_once_with("123")

    def test_write_plus_one_to_db(self):
        database = Database()

        with (
            patch.object(database, "read", return_value=123) as read_mock,
            patch.object(database, "write") as write_mock,
        ):
            database.write_plus_one_to_db()

            read_mock.assert_called_once_with()
            write_mock.assert_called_once_with(124)
