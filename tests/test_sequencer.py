from unittest.mock import Mock, patch

from dragnote.sequencer import Sequencer


class TestSequencer:
    @patch("dragnote.sequencer.pygame.midi.Output")
    def test_init(self, output_mock):
        synth_num = Mock()
        instrument_num = Mock()
        volume = Mock()
        tempo = Mock()

        sequencer = Sequencer(synth_num, instrument_num, volume, tempo)

        assert sequencer.synth_num == synth_num
        assert sequencer.volume == volume
        assert sequencer.tempo == tempo
        output_mock.assert_called_once_with(synth_num)
        assert sequencer.midi_out == output_mock.return_value
        sequencer.midi_out.set_instrument.assert_called_once_with(instrument_num)

    @patch("dragnote.sequencer.pygame.time.wait")
    @patch("dragnote.sequencer.pygame.midi.Output")
    def test_play_harmony(self, output_mock, wait_mock):
        synth_num = Mock()
        instrument_num = Mock()
        volume = Mock()
        tempo = Mock()
        sequencer = Sequencer(synth_num, instrument_num, volume, tempo)
        harmony = Mock(
            notes=[
                Mock(),
                Mock(),
                Mock(),
            ],
            get_duration_in_seconds=Mock(return_value=2),
        )

        sequencer.play_harmony(harmony)

        harmony.notes[0].to_note_value.assert_called_with()
        harmony.notes[1].to_note_value.assert_called_with()
        harmony.notes[2].to_note_value.assert_called_with()

        harmony.get_duration_in_seconds.assert_called_once_with(tempo)

        assert sequencer.midi_out.note_on.call_count == 3
        sequencer.midi_out.note_on.assert_any_call(harmony.notes[0].to_note_value.return_value, sequencer.volume)
        sequencer.midi_out.note_on.assert_any_call(harmony.notes[1].to_note_value.return_value, sequencer.volume)
        sequencer.midi_out.note_on.assert_any_call(harmony.notes[2].to_note_value.return_value, sequencer.volume)

        wait_mock.assert_called_once_with(2000)

        assert sequencer.midi_out.note_off.call_count == 3
        sequencer.midi_out.note_off.assert_any_call(harmony.notes[0].to_note_value.return_value, sequencer.volume)
        sequencer.midi_out.note_off.assert_any_call(harmony.notes[1].to_note_value.return_value, sequencer.volume)
        sequencer.midi_out.note_off.assert_any_call(harmony.notes[2].to_note_value.return_value, sequencer.volume)

    @patch("dragnote.sequencer.pygame.midi.Output")
    def test_play_composition(self, output_mock):
        synth_num = Mock()
        instrument_num = Mock()
        volume = Mock()
        tempo = Mock()
        sequencer = Sequencer(synth_num, instrument_num, volume, tempo)
        composition = [Mock(), Mock(), Mock()]

        with patch.object(sequencer, "play_harmony") as play_harmony_mock:
            sequencer.play_composition(composition)

            assert play_harmony_mock.call_count == 3
            play_harmony_mock.assert_any_call(composition[0])
            play_harmony_mock.assert_any_call(composition[1])
            play_harmony_mock.assert_any_call(composition[2])
