import logging

from dragnote.database import read, write
from dragnote.domain import Harmony, Note
from dragnote.parse import parse_composition
from dragnote.sequencer import Sequencer
from dragnote.sounds import Sounds, play_sound

logger = logging.getLogger(__name__)


def harmony_str_to_notes_set(harmony: str) -> set[Note]:
    notes = {Note.from_str(note_str) for note_str in harmony.split(":")}
    return notes


def get_notes_list_from_str(input_notes: str) -> list[Note]:
    note_list = harmony_str_to_notes_set(input_notes)
    note_list = [s for s in note_list if s]  # todo: use normal name against "s"
    return note_list


def play(synth_num: int):
    sequencer = Sequencer(synth_num, 0)

    while True:
        composition_num = read()
        composition = parse_composition(composition_num)
        print("Composition name is", composition.name)
        print("Tonality is", composition.tonality)
        sequencer.play_composition(composition)

        errors_count = 0

        for i, harmony in enumerate(composition.voice.harmonies):
            while errors_count < 3:  # todo: remove magic number
                input_notes = input(f"Enter {i} notes (errors: {errors_count}):")
                new_notes_list = get_notes_list_from_str(input_notes)
                values = {note.to_note_value() for note in harmony.notes}
                input_values = {note.to_note_value() for note in new_notes_list}
                result = values == input_values
                sequencer.play_harmony(Harmony(notes=tuple(new_notes_list), duration=harmony.duration), tempo=composition.tempo)
                if result:
                    play_sound(Sounds.OVER)
                    break
                else:
                    play_sound(Sounds.PEEP)
                    errors_count += 1
            else:
                play_sound(Sounds.FAIL)
                break
        else:
            play_sound(Sounds.BULK)
            write(composition_num + 1)
            continue

        play_sound(Sounds.DZIN)
