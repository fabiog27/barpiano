import sys
from helpers.chordmatcher import do_chords_sequences_match
import threading

from typing import List


class Device(object):

    def __init__(
            self,
            name: str,
            note_sequences: List[List[str]],
            chord_sequences: List[List[List[str]]],
    ):
        self.times_run = 0
        self.is_running = False
        self.note_sequences = note_sequences
        self.chord_sequences = chord_sequences
        self.name = name

    def check(self, note_history: List[str], chord_history: List[List[str]]) -> bool:
        trigger_note_sequence = self.check_note_history(note_history)
        trigger_chord_sequence = self.check_chord_history(chord_history)
        if trigger_note_sequence != [] or trigger_chord_sequence != []:
            if not self.is_running:
                self.is_running = True
                print('Device "', self.name, '" triggered', sep='')
                device_thread = threading.Thread(
                    target=self.trigger,
                    args=(trigger_note_sequence, trigger_chord_sequence,)
                )
                device_thread.start()
                sys.stdout.flush()
                return True
            else:
                print('Device "', self.name, '" can\'t be run multiple times at once!', sep='')
                sys.stdout.flush()
                return True

    def check_note_history(self, note_history: List[str]) -> List[str]:
        for note_sequence in self.note_sequences:
            if len(note_history) < len(note_sequence):
                continue
            if note_history[-len(note_sequence):] == note_sequence:
                return note_sequence
        return []

    def check_chord_history(self, chord_history: List[List[str]]) -> List[List[str]]:
        for chord_sequence in self.chord_sequences:
            if len(chord_history) < len(chord_sequence):
                continue
            relevant_history = chord_history[-len(chord_sequence):]
            if do_chords_sequences_match(relevant_history, chord_sequence):
                return chord_sequence
        return []

    def finish(self):
        self.times_run += 1
        self.is_running = False
        text = self.name + ' has run ' + str(self.times_run)
        text += ' time' if self.times_run == 1 else ' times'
        print(text)
        sys.stdout.flush()

    def trigger(self, note_sequence, chord_sequence):
        pass

    def on_engage_bar_mode(self) -> None:
        pass

    def on_disengage_bar_mode(self) -> None:
        pass

    def start_up(self) -> bool:
        pass

    def shut_down(self) -> bool:
        pass
