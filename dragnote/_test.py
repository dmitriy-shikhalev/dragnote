# # SPDX-FileCopyrightText: 2013 Ole Martin Bjorndalen <ombdalen@gmail.com>
# #
# # SPDX-License-Identifier: MIT
#
# """
# First example from here modified to use Mido messages:
#
#     http://pypi.python.org/pypi/python-rtmidi/
# """
# import time
#
# import rtmidi
#
# import mido
#
# midiout = rtmidi.RtMidiOut()
# ports_count = midiout.getPortCount()
#
# print("ports_count", ports_count)
# if ports_count:
#     midiout.openPort(0)
# else:
#     midiout.openVirtualPort("My virtual output")
#
# # Original example:
# # note_on = [0x99, 60, 112] # channel 10, middle C, velocity 112
# # note_off = [0x89, 60, 0]
#
# note_on = rtmidi.MidiMessage('note_on', channel=9, note=60, velocity=112)
# note_off = rtmidi.MidiMessage('note_off', channel=9, note=60, velocity=0)
# midiout.sendMessage(note_on[0])
# time.sleep(0.5)
# midiout.sendMessage(note_off)
#
# del midiout

import time

import mido

# Create a MIDI message
msg = mido.Message('note_on', note=60, velocity=64)
print(mido.get_output_names())

# Open an output port and send the message
print("first")
for name in mido.get_output_names():
    with mido.open_output(name) as port:
        print("second", name)
        port.send(msg)
        time.sleep(0.5)

# # Read messages from an input port
# with mido.open_input('Midi Through:Midi Through Port-0 14:0') as inport:
#     for msg in inport:
#         print(msg)