from unittest.mock import Mock

from dragnote.compare import Compare


class TestCompare:
    def test_init(self):
        left = Mock()
        right = Mock()
        compare = Compare(left, right)
        left.__eq__ = Mock()

        assert compare.is_equal()

        left.__eq__.assert_called_once_with(right)
