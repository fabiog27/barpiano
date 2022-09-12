import re
from typing import List

import serial

from helpers.serial_connection import send_arduino_message

PIXEL_AMOUNT = 296
NOTE_AMOUNT = 78

DOUBLE_LED_NOTE_AMOUNT = 16
FIRST_OCTAVE_PIXEL_COUNT = 12 * 2
SECOND_OCTAVE_DOUBLE_LED_PIXEL_COUNT = (DOUBLE_LED_NOTE_AMOUNT - 12) * 2
SECOND_OCTAVE_PIXEL_COUNT = SECOND_OCTAVE_DOUBLE_LED_PIXEL_COUNT + (12 - (DOUBLE_LED_NOTE_AMOUNT - 12)) * 4
NORMAL_OCTAVE_PIXEL_COUNT = 12 * 4
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

KIK_BLUE = (0, 64, 192)
KIK_ORANGE = (255, 134, 0)


class LEDController(object):

    def __init__(self, serial_identifier: str):
        self.serial_connection = serial.Serial(serial_identifier, baudrate=921600, timeout=0.001)
        self.note_splitter = re.compile(r"([A-Z]#?)(\d)")
        self.init_leds()

    def activate_note(self, full_note_name):
        corresponding_leds = self.map_note_to_pixel_numbers(full_note_name)
        message = 'A{:03d}{:03d}{:03d}{:03d}{:03d}ZX'.format(
            corresponding_leds[0],
            corresponding_leds[-1],
            KIK_ORANGE[0],
            KIK_ORANGE[1],
            KIK_ORANGE[2]
        )
        send_arduino_message(self.serial_connection, message)

    def deactivate_note(self, full_note_name):
        corresponding_leds = self.map_note_to_pixel_numbers(full_note_name)
        message = 'A{:03d}{:03d}{:03d}{:03d}{:03d}ZX'.format(
            corresponding_leds[0],
            corresponding_leds[-1],
            KIK_BLUE[0],
            KIK_BLUE[1],
            KIK_BLUE[2]
        )
        send_arduino_message(self.serial_connection, message)

    def init_leds(self):
        message = 'A{:03d}{:03d}{:03d}{:03d}{:03d}ZX'.format(
            0,
            PIXEL_AMOUNT - 1,
            KIK_BLUE[0],
            KIK_BLUE[1],
            KIK_BLUE[2],
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


if __name__ == '__main__':
    serial_identifier = '/dev/cu.usbserial-143220'
    led_controller = LEDController(serial_identifier=serial_identifier)
    led_controller.activate_note('G7')
    print('go ahead')
