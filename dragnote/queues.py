from queue import Queue

from dragnote.domain import Note
from dragnote.errors import EmptyString
from dragnote.iofuncs import read_input
from dragnote.parse import parse_notes_row


class InputQueue:
    def __init__(self):
        self.queue: Queue[set[Note]] = Queue()

    def _read(self):
        string = read_input()
        if not string.strip():
            raise EmptyString
        for notes_set in parse_notes_row(string):
            self.queue.put(notes_set)

    def get(self) -> set[Note]:
        if not self.queue.qsize():
            self._read()
        return self.queue.get()
