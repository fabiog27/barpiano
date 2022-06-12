import sys
from typing import List

from devices.device import Device
from helpers.chordmatcher import do_chords_sequences_match


class Controller(object):
    BAR_MODE_CHORD_SEQUENCE = [['D', 'E'], ['D', 'E'], ['G', 'A']]

    def __init__(self):
        self.devices: List[Device] = []
        self.is_in_bar_mode: bool = False
        self.is_bar_mode_ready: bool = False

    def add_device(self, device: Device):
        self.devices.append(device)

    def check(self, note_history: List[str], chord_history: List[List[str]]):
        is_trigger = self.is_trigger_chord_sequence(chord_history)

        if not self.is_in_bar_mode:
            if is_trigger:
                self.start_bar_mode()
            return
        elif self.is_in_bar_mode and is_trigger:
            self.end_bar_mode()
            return

        for device in self.devices:
            was_triggered = device.check(note_history, chord_history)
            if was_triggered:
                break

    def is_trigger_chord_sequence(self, chord_history):
        if len(chord_history) < len(self.BAR_MODE_CHORD_SEQUENCE):
            return False
        relevant_history = chord_history[-len(self.BAR_MODE_CHORD_SEQUENCE):]
        return do_chords_sequences_match(relevant_history, self.BAR_MODE_CHORD_SEQUENCE)

    def start_bar_mode(self):
        print('Starting bar mode')
        sys.stdout.flush()
        self.is_in_bar_mode = True
        for device in self.devices:
            device.on_engage_bar_mode()

    def end_bar_mode(self):
        print('Ending bar mode')
        sys.stdout.flush()
        self.is_in_bar_mode = False
        for device in self.devices:
            device.on_disengage_bar_mode()
