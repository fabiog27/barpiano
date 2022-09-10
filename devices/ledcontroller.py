import re
from typing import List

import board
import neopixel

PIXEL_AMOUNT = 296
NOTE_AMOUNT = 78

SINGLE_LED_NOTE_AMOUNT = 16
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

KIK_BLUE = (0, 64, 192)
KIK_ORANGE = (255, 134, 0)


class LEDController(object):

    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.D6, PIXEL_AMOUNT)
        self.active_notes: List[str] = []
        self.note_splitter = re.compile(r"([A-Z]#?)(\d)")
        self.update_leds()

    def update_active_notes(self, active_notes: List[str]):
        self.active_notes = active_notes
        self.update_leds()

    def update_leds(self):
        active_leds: List[int] = []
        for active_note in self.active_notes:
            active_leds.extend(self.map_note_to_pixel_numbers(active_note))
        for i in range(PIXEL_AMOUNT):
            if i in active_leds:
                self.pixels[i] = KIK_ORANGE
            else:
                self.pixels[i] = KIK_BLUE

    def map_note_to_pixel_numbers(self, full_note_name) -> List[int]:
        split_note = self.note_splitter.match(full_note_name).groups()
        short_name = split_note[0]
        octave = split_note[1]
        if octave == 1:
            return [NOTES.index(short_name)]
        if octave == 2:
            index = NOTES.index(short_name)
            if index < 4:
                return [11 + index]
            else:
                first_pixel = 15 + 2 * (index - 3)

        else:
            first_pixel = 2 * ((12 * (octave - 1)) - 1 + NOTES.index(short_name)) - 15
            return [first_pixel, first_pixel + 1]
