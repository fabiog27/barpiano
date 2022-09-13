from typing import List

from ledcontroller.led_controller import LEDController
from triggerables.games.game import Game


class SingleNoteController(object):

    def __init__(self, led_controller: LEDController):
        self.games: List[Game] = []
        self.led_controller = led_controller

    def activate_note(self, full_note_name):
        self.led_controller.activate_note(full_note_name)
        for game in self.games:
            if game.is_running:
                game.activate_note(full_note_name)

    def deactivate_note(self, full_note_name):
        self.led_controller.deactivate_note(full_note_name)
        for game in self.games:
            if game.is_running:
                game.deactivate_note(full_note_name)

    def add_game(self, game: Game):
        self.games.append(game)
