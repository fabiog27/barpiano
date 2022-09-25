import re
import time
from typing import List, Tuple

from constants.leds import LEDS
from constants.theme import Theme
from helpers.notes import NOTES
from ledcontroller.led_message_manager import LEDMessageManager, LEDMessage


class LEDController(object):

    def __init__(self, serial_identifier: str):
        self.note_splitter = re.compile(r"([A-Z]#?)(\d)")
        self.are_note_interactions_active = True
        self.message_manager = LEDMessageManager(serial_identifier)
        self.message_manager.start()
        time.sleep(0.5)
        self.init_leds(Theme.background_color)

    def show_loading_sequence(self, duration_in_s: int):
        self.init_leds(Theme.inactive_color)
        interval = duration_in_s / LEDS.PIXEL_AMOUNT
        for i in range(LEDS.PIXEL_AMOUNT):
            message = LEDMessage(i, i, Theme.active_color)
            self.message_manager.add_message(message)
            time.sleep(interval)
        self.blink(Theme.background_color, Theme.active_color, 2)
        self.init_leds(Theme.background_color)

    def show_success_flash(self):
        self.blink(Theme.active_color, Theme.inactive_color)

    def show_failure_flash(self):
        self.blink(Theme.failure_color, Theme.inactive_color, 10, 0.1)
        self.init_leds(Theme.background_color)

    def blink(self, color_a: Tuple[int, int, int], color_b: Tuple[int, int, int], times=3, interval=0.2):
        for i in range(times):
            self.init_leds(color_a)
            time.sleep(interval)
            self.init_leds(color_b)
            time.sleep(interval)

    def set_range_to(self, starting_note: str, ending_note: str, color: Tuple[int, int, int]):
        starting_led = self.map_note_to_pixel_numbers(starting_note)[0]
        ending_led = self.map_note_to_pixel_numbers(ending_note)[-1]
        purpose = 'set range from {0} to {1} to color'.format(starting_note, ending_note)
        message = LEDMessage(starting_led, ending_led, color, purpose)
        self.message_manager.add_message(message)

    def set_note_to(self, full_note_name, color: Tuple[int, int, int], purpose=''):
        corresponding_leds = self.map_note_to_pixel_numbers(full_note_name)
        purpose_info = purpose if purpose != '' else 'set ' + full_note_name
        message = LEDMessage(corresponding_leds[0], corresponding_leds[-1], color, purpose_info)
        self.message_manager.add_message(message)

    def activate_note(self, full_note_name):
        self.set_note_to(full_note_name, Theme.accent_color, 'activate ' + full_note_name)

    def deactivate_note(self, full_note_name):
        self.set_note_to(full_note_name, Theme.background_color, 'deactivate ' + full_note_name)

    def init_leds(self, color: Tuple[int, int, int]):
        message = LEDMessage(0, LEDS.PIXEL_AMOUNT - 1, color)
        self.message_manager.add_message(message)

    def map_note_to_pixel_numbers(self, full_note_name) -> List[int]:
        split_note = self.note_splitter.match(full_note_name).groups()
        short_name = split_note[0]
        octave = int(split_note[1])
        if octave == 1:
            first_pixel = 2 * NOTES.index(short_name)
            return [first_pixel, first_pixel + 1]
        if octave == 2:
            index = NOTES.index(short_name)
            if index < 4:
                first_pixel = LEDS.FIRST_OCTAVE_PIXEL_COUNT + 2 * index
                return [first_pixel, first_pixel + 1]
            else:
                first_pixel = LEDS.FIRST_OCTAVE_PIXEL_COUNT + LEDS.SECOND_OCTAVE_DOUBLE_LED_PIXEL_COUNT + 4 * (index - 4)
                return [first_pixel + i for i in range(4)]

        else:
            first_pixel = LEDS.FIRST_OCTAVE_PIXEL_COUNT + LEDS.SECOND_OCTAVE_PIXEL_COUNT + (
                    octave - 3) * 4 * 12 + 4 * NOTES.index(short_name)
            return [first_pixel + i for i in range(4)]
