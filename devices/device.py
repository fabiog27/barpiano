import sys
import threading
import time

from typing import List


class Device(object):

    def __init__(self, name: str, gpio_pin_number: int, duration: int, note_sequence: List[str]):
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
        self.name = name

    def check(self, note_history: List[str]):
        if len(note_history) < len(self.note_sequence):
            return
        if note_history[-len(self.note_sequence):] == self.note_sequence:
            if not self.is_running:
                self.is_running = True
                print('Device "', self.name, '" triggered', sep='')
                device_thread = threading.Thread(target=self.trigger)
                device_thread.start()
            else:
                print('Device "', self.name, '" can\'t be run multiple times at once!', sep='')

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
