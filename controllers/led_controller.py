import re
import time
from typing import List, Tuple

import serial

from constants.colors import MELLOW_WHITE, KIK_BLUE, KIK_ORANGE, ACTIVE_GREEN, MOLE
from helpers.notes import NOTES
from helpers.serial_connection import send_arduino_message

PIXEL_AMOUNT = 296
NOTE_AMOUNT = 78

DOUBLE_LED_NOTE_AMOUNT = 16
FIRST_OCTAVE_PIXEL_COUNT = 12 * 2
SECOND_OCTAVE_DOUBLE_LED_PIXEL_COUNT = (DOUBLE_LED_NOTE_AMOUNT - 12) * 2
SECOND_OCTAVE_PIXEL_COUNT = SECOND_OCTAVE_DOUBLE_LED_PIXEL_COUNT + (12 - (DOUBLE_LED_NOTE_AMOUNT - 12)) * 4
NORMAL_OCTAVE_PIXEL_COUNT = 12 * 4


class LEDController(object):

    def __init__(self, serial_identifier: str):
        self.serial_connection = serial.Serial(serial_identifier, baudrate=921600, timeout=0.001)
        self.note_splitter = re.compile(r"([A-Z]#?)(\d)")
        self.message_template = 'A{:03d}{:03d}{:03d}{:03d}{:03d}ZX'
        self.init_leds(KIK_BLUE)
        self.are_note_interactions_active = True

    def show_loading_sequence(self, duration_in_s: int):
        self.init_leds(MELLOW_WHITE)
        interval = duration_in_s / PIXEL_AMOUNT
        for i in range(PIXEL_AMOUNT):
            message = self.message_template.format(i, i, ACTIVE_GREEN[0], ACTIVE_GREEN[1], ACTIVE_GREEN[2])
            send_arduino_message(self.serial_connection, message)
            time.sleep(interval)
        self.blink(KIK_BLUE, ACTIVE_GREEN, 2)
        self.init_leds(KIK_BLUE)

    def show_success_flash(self):
        self.blink(ACTIVE_GREEN, MELLOW_WHITE)

    def show_failure_flash(self):
        self.blink(MOLE, MELLOW_WHITE, 10, 0.1)
        self.init_leds(KIK_BLUE)

    def blink(self, color_a: Tuple[int, int, int], color_b: Tuple[int, int, int], times=3, interval=0.2):
        for i in range(times):
            self.init_leds(color_a)
            time.sleep(interval)
            self.init_leds(color_b)
            time.sleep(interval)

    def set_note_to(self, full_note_name, color: Tuple[int, int, int]):
        corresponding_leds = self.map_note_to_pixel_numbers(full_note_name)
        message = self.message_template.format(
            corresponding_leds[0],
            corresponding_leds[-1],
            color[0],
            color[1],
            color[2]
        )
        send_arduino_message(self.serial_connection, message)

    def activate_note(self, full_note_name):
        self.set_note_to(full_note_name, KIK_ORANGE)

    def deactivate_note(self, full_note_name):
        corresponding_leds = self.map_note_to_pixel_numbers(full_note_name)
        message = self.message_template.format(
            corresponding_leds[0],
            corresponding_leds[-1],
            KIK_BLUE[0],
            KIK_BLUE[1],
            KIK_BLUE[2]
        )
        send_arduino_message(self.serial_connection, message)

    def init_leds(self, color: Tuple[int, int, int]):
        message = self.message_template.format(
            0,
            PIXEL_AMOUNT - 1,
            color[0],
            color[1],
            color[2],
        )
        send_arduino_message(self.serial_connection, message)

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
                first_pixel = FIRST_OCTAVE_PIXEL_COUNT + 2 * index
                return [first_pixel, first_pixel + 1]
            else:
                first_pixel = FIRST_OCTAVE_PIXEL_COUNT + SECOND_OCTAVE_DOUBLE_LED_PIXEL_COUNT + 4 * (index - 4)
                return [first_pixel + i for i in range(4)]

        else:
            first_pixel = FIRST_OCTAVE_PIXEL_COUNT + SECOND_OCTAVE_PIXEL_COUNT + (
                    octave - 3) * 4 * 12 + 4 * NOTES.index(short_name)
            return [first_pixel + i for i in range(4)]
