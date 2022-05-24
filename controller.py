from typing import List

from devices.device import Device


class Controller(object):
    BAR_MODE_CHORD_SEQUENCE = [['D', 'E'], ['D', 'E'], ['G', 'A']]

    def __init__(self):
        self.devices: List[Device] = []
        self.is_in_bar_mode: bool = False
        self.is_bar_mode_starting: bool = False

    def add_device(self, device: Device):
        self.devices.append(device)

    def check(self, note_history: List[str], chord_history: List[List[str]]):
        is_trigger_chord_sequence = len(chord_history) > len(Controller.BAR_MODE_CHORD_SEQUENCE) and chord_history[-len(
            Controller.BAR_MODE_CHORD_SEQUENCE
        ):] == Controller.BAR_MODE_CHORD_SEQUENCE

        if not self.is_in_bar_mode and is_trigger_chord_sequence:
            self.start_bar_mode()
            return
        elif self.is_in_bar_mode and is_trigger_chord_sequence:
            self.end_bar_mode()
            return

        for device in self.devices:
            was_triggered = device.check(note_history, chord_history)
            if was_triggered:
                break

    def start_bar_mode(self):
        self.is_in_bar_mode = True
        for device in self.devices:
            device.start_up()

    def end_bar_mode(self):
        self.is_in_bar_mode = False
        for device in self.devices:
            device.shut_down()
