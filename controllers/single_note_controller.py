from games.whackamole import WhackAMole
from helpers.notes import get_position_from_full_note_name


class SingleNoteController(object):

    def __init__(self, whack_a_mole: WhackAMole):
        self.whack_a_mole = whack_a_mole

    def handle_note(self, full_note_name):
        position = get_position_from_full_note_name(full_note_name)
        if self.whack_a_mole.is_running:
            self.whack_a_mole.try_to_whack_mole(position)
