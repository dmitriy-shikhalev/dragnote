import logging

from dragnote.domain import Note
from dragnote.parse import parse_composition
from dragnote.sequencer import Sequencer

logger = logging.getLogger(__name__)


def harmony_str_to_notes_set(harmony: str) -> set[int]:
    notes = {Note.from_str(note_str).get_event_value() for note_str in harmony.split(":")}
    return notes


def get_notes_list_from_str(input_notes: str) -> list[set[int]]:
    harmonies: list[str] = input_notes.split(" ")
    notes_list = [harmony_str_to_notes_set(harmony) for harmony in harmonies]
    notes_list = [s for s in notes_list if s]  # todo: use normal name against "s"
    return notes_list


def play(composition_name: str, synth_num: int, instrument_num: int):
    composition = parse_composition(composition_name)
    sequencer = Sequencer(synth_num, instrument_num)
    print("Composition name is", composition.name)
    print("Tonality is", composition.tonality)
    sequencer.play_composition(composition)
    schedule = composition.to_schedule()

    input_notes = input("Enter notes: ")
    new_notes_list = get_notes_list_from_str(input_notes)
    old_notes_list = schedule.get_notes_list()
    result = new_notes_list == old_notes_list
    if result:
        print("Ok!")
        sequencer.play_schedule(schedule)
    else:
        print("Wrong!")
        new_schedule = schedule.substitute(new_notes_list)
        sequencer.play_schedule(new_schedule)
