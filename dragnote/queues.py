from queue import Queue

from dragnote.domain import Harmony, Note
from dragnote.errors import EmptyInput
from dragnote.iofuncs import read_input
from dragnote.parse import parse_notes_row


class InputQueue:
    def __init__(self):
        self.queue: Queue[set[Note]] = Queue()

    def _read(self, notes_list: list[list[Note]] = None, first_note: Harmony = None):
        if notes_list is None and first_note is None:
            raise ValueError("First note is None and notes is None")
        string = read_input(notes_list=notes_list, first_note=first_note)
        if not string.strip():
            raise EmptyInput
        for notes_set in parse_notes_row(string):
            self.queue.put(notes_set)

    def get(self, first_note: Harmony = None, notes_list: list[list[Note]] = None) -> set[Note]:
        if not self.queue.qsize():
            self._read(first_note=first_note, notes_list=notes_list)
        return self.queue.get()
