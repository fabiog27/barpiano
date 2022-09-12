import math
import re

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
note_splitter = re.compile(r"([A-Z]#?)(\d)")


def get_full_note_name_from_position(position: int):
    if position < 0 or position > 77:
        raise Exception("Position out of range")
    octave = math.floor(position / 12) + 1
    offset = position % 12
    return "{}{}".format(NOTES[offset], octave)


def get_position_from_full_note_name(full_note_name: str):
    split_note = note_splitter.match(full_note_name).groups()
    short_name = split_note[0]
    octave = int(split_note[1]) - 1
    return octave * 12 + NOTES.index(short_name)
