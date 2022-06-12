from devices.device import Device
import gpiozero
import time
import sys

from typing import List

ACCESS_SEQUENCE = ['A', 'C', 'C', 'E', 'D#', 'D#']  # Access


class Lock(Device):

    GPIO_PIN = 20
    TRIGGER_TIME_MS = 1000

    def __init__(self):
        super().__init__('Lock', [ACCESS_SEQUENCE], [])
        self.lock_trigger = gpiozero.DigitalOutputDevice(self.GPIO_PIN, active_high=False, initial_value=False)

    def on_engage_bar_mode(self) -> None:
        self.release_lock()

    def release_lock(self) -> None:
        print('Releasing lock')
        self.lock_trigger.on()
        time.sleep(self.TRIGGER_TIME_MS / 1000)
        self.lock_trigger.off()
        print('Lock released')
        sys.stdout.flush()

    def trigger(self, note_sequence: List[str], chord_sequence: List[List[str]]) -> None:
        if note_sequence == ACCESS_SEQUENCE:
            self.release_lock()
