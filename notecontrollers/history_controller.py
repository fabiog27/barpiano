import sys
from typing import List

from helpers.chordmatcher import do_chords_sequences_match
from triggerables.triggerable import Triggerable


class HistoryController(object):
    BAR_MODE_CHORD_SEQUENCE = [['D', 'E'], ['D', 'E'], ['G', 'A']]

    def __init__(self):
        self.triggerables: List[Triggerable] = []
        self.is_in_bar_mode = False

    def add_triggerable(self, device: Triggerable):
        self.triggerables.append(device)

    def check(self, note_history: List[str], chord_history: List[List[str]]):
        is_trigger = self.is_trigger_chord_sequence(chord_history)

        if not self.is_in_bar_mode and is_trigger:
            self.start_bar_mode()
            return
        elif self.is_in_bar_mode and is_trigger:
            self.end_bar_mode()
            return

        for triggerable in self.triggerables:
            was_triggered = triggerable.check(note_history, chord_history)
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
        for triggerable in self.triggerables:
            triggerable.on_engage_bar_mode()

    def end_bar_mode(self):
        print('Ending bar mode')
        sys.stdout.flush()
        self.is_in_bar_mode = False
        for triggerable in self.triggerables:
            triggerable.on_disengage_bar_mode()
