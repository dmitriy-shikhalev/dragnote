from unittest.mock import Mock, patch

import pytest

from dragnote.queues import InputQueue


class TestInputQueue:
    @patch("dragnote.queues.Queue")
    def test_init(self, queue_mock):
        input_queue = InputQueue()

        queue_mock.assert_called_once_with()
        assert input_queue.queue == queue_mock.return_value

    @patch("dragnote.queues.read_input", return_value="")
    def test_read_empty(self, read_input_mock):
        input_queue = InputQueue()

        with pytest.raises(ValueError):
            input_queue._read()

    @patch("dragnote.queues.parse_notes_row", return_value=[Mock(), Mock(), Mock()])
    @patch("dragnote.queues.read_input", return_value="C1:D1 E1")
    def test_read_not_empty(self, read_input_mock, parse_notes_row_mock):
        input_queue = InputQueue()

        with patch.object(input_queue, "queue") as queue_mock:
            input_queue._read()

            read_input_mock.assert_called_once_with()
            parse_notes_row_mock.assert_called_once_with("C1:D1 E1")

            assert queue_mock.put.call_count == 3
            queue_mock.put.assert_any_call(parse_notes_row_mock.return_value[0])
            queue_mock.put.assert_any_call(parse_notes_row_mock.return_value[1])
            queue_mock.put.assert_any_call(parse_notes_row_mock.return_value[2])

    def test_get_not_empty(self):
        input_queue = InputQueue()

        with patch.object(input_queue, "queue", Mock(qsize=Mock(return_value=1))) as queue_mock:
            result = input_queue.get()

            queue_mock.qsize.assert_called_once_with()
            queue_mock.get.assert_called_once_with()
            assert result == queue_mock.get.return_value

    def test_get_empty(self):
        input_queue = InputQueue()

        with (
            patch.object(input_queue, "queue", Mock(qsize=Mock(return_value=0))) as queue_mock,
            patch.object(input_queue, "_read") as _read_mock,
        ):
            result = input_queue.get()

            queue_mock.qsize.assert_called_once_with()
            _read_mock.assert_called_once_with()
            queue_mock.get.assert_called_once_with()
            assert result == queue_mock.get.return_value
