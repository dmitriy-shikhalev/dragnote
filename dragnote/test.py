import time

import pygame
import pygame.midi

# pygame.init()
pygame.midi.init()

# Get the default MIDI output device ID
default_output_id = pygame.midi.get_default_output_id()
print("count", pygame.midi.get_count())

if default_output_id == -1:
    print("No default MIDI output device found.")
    pygame.quit()
else:
    for i in range(pygame.midi.get_count()):
        # pygame.midi.init()
        if i in {0, 1,}:
            print('pass')
            continue
        print('midi out id', i)
        print(f"Using MIDI device: {pygame.midi.get_device_info(i)}")


        # Create a MIDI output object
        midi_out = pygame.midi.Output(i)


        def play_note(note: int):
            midi_out.note_on(note, 127, channel=0)
            time.sleep(0.3)  # Wait for 1 second
            midi_out.note_off(note, 127)  # Turn off the note
        # Send MIDI note-on and note-off messages
        # Note: This requires a synthesizer/sound module to produce audible sound [8]

        print(pygame.midi.midi_to_ansi_note(60))
        midi_out.note_on(60, 127, channel=0)
        print(pygame.midi.midi_to_ansi_note(63))
        midi_out.note_on(63, 127, channel=0)
        midi_out.note_on(67, 127, channel=0)
        print(pygame.midi.midi_to_ansi_note(67))

        time.sleep(3)

        midi_out.note_off(60, 127)
        midi_out.note_off(63, 127)
        midi_out.note_off(67, 127)
        print('stop')


        del midi_out
        pygame.midi.quit()