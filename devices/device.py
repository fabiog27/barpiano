import sys
import threading
import time
import serial

from typing import List, Optional


class Device(object):

    def __init__(
            self,
            name: str,
            gpio_pin_number: int,
            duration: int,
            note_sequence: List[str],
            chord_sequence: Optional[List[List[str]]],
    ):
        """
        :param name:
        :param gpio_pin_number:
        :param duration:
        :param note_sequence:
        """
        self.times_run = 0
        self.is_running = False
        self.duration = duration
        self.pin_number = gpio_pin_number
        self.note_sequence = note_sequence
        self.chord_sequence = chord_sequence
        self.name = name

    def check(self, note_history: List[str], chord_history: List[List[str]]) -> bool:
        is_trigger_note_sequence = self.check_note_history(note_history)
        is_trigger_chord_sequence = self.check_chord_history(chord_history)
        if is_trigger_note_sequence or is_trigger_chord_sequence:
            if not self.is_running:
                self.is_running = True
                print('Device "', self.name, '" triggered', sep='')
                device_thread = threading.Thread(target=self.trigger)
                device_thread.start()
                return True
            else:
                print('Device "', self.name, '" can\'t be run multiple times at once!', sep='')
                return True

    def check_note_history(self, note_history: List[str]) -> bool:
        if len(note_history) < len(self.note_sequence):
            return False
        return note_history[-len(self.note_sequence):] == self.note_sequence

    def check_chord_history(self, chord_history: List[List[str]]) -> bool:
        if self.chord_sequence is None:
            return False
        if len(chord_history) < len(self.chord_sequence):
            return False
        return chord_history[-len(self.chord_sequence):] == self.chord_sequence

    def finish(self):
        self.times_run += 1
        self.is_running = False
        text = self.name + ' has run ' + str(self.times_run)
        text += ' time' if self.times_run == 1 else ' times'
        print(text)
        sys.stdout.flush()

    def wait(self):
        for i in range(self.duration):
            print('\r', end='')
            print('[' + (i + 1) * '*' + (self.duration - i - 1) * '-' + ']', end='')
            time.sleep(0.5)
            time.sleep(0.5)
        print()

    def trigger(self):
        pass

    def start_up(self):
        pass

    def shut_down(self):
        pass
