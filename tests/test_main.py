from unittest.mock import Mock, patch

from dragnote.main import main


@patch("dragnote.main.Game")
@patch(
    "dragnote.main.Settings",
    return_value=Mock(
        log_level="INFO",
    ),
)
def test_main(settings_mock, game_mock):
    main()

    settings_mock.assert_called_once_with()
    game_mock.assert_called_once_with(settings_mock.return_value)
    game_mock.return_value.run.assert_called_once_with()
