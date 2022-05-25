from collections import Counter

from typing import List


def do_chords_sequences_match(sequence_1: List[List[str]], sequence_2: List[List[str]]) -> bool:
    if len(sequence_1) != len(sequence_2):
        return False
    for i in range(len(sequence_1)):
        chord_1 = sequence_1[i]
        chord_2 = sequence_2[i]
        if not are_chords_equal(chord_1, chord_2):
            return False
    return True


def are_chords_equal(chord_1: List[str], chord_2: List[str]) -> bool:
    return Counter(chord_1) == Counter(chord_2)
