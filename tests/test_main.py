import pytest

from blank_project.main import function


def test_blank_function():
    """Test blank function."""
    with pytest.raises(ZeroDivisionError):
        function()
