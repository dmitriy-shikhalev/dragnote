import logging

from dragnote.domain import Note
from dragnote.parse import parse_composition
from dragnote.sequencer import Sequencer

logger = logging.getLogger(__name__)


def harmony_str_to_notes_set(harmony: str):
    notes = [Note.from_str(note_str) for note_str in harmony.split(":")]
    return notes

def get_note_iter_from_str(input_notes: str):
    harmonies: list[str] = input_notes.split(" ")
    notes_list = [
        harmony_str_to_notes_set(harmony)
        for harmony in harmonies
    ]
    return notes_list


def play(composition_name: str, synth_num: int, instrument_num: int):
    composition = parse_composition(composition_name)
    sequencer = Sequencer(synth_num, instrument_num)
    sequencer.play_composition(composition)
    schedule = composition.to_schedule()

    input_notes = input("Enter notes: ")
    notes = get_note_iter_from_str(input_notes)
    new_schedule = schedule.substitute(notes)

    sequencer.play_schedule(new_schedule)
    raise NotImplementedError(schedule == new_schedule)
