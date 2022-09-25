import math
import random
import time
from threading import Thread, Lock
from typing import List, Optional

from constants.theme import Theme
from ledcontroller.led_controller import LEDController
from helpers.notes import get_full_note_name_from_position, get_position_from_full_note_name
from triggerables.games.game import Game

MIN_PLAYABLE = 'E2'
MAX_PLAYABLE = 'F7'

START_INDEX = get_position_from_full_note_name(MIN_PLAYABLE)
END_INDEX = get_position_from_full_note_name(MAX_PLAYABLE)

SCORE_DIFFICULTY_STEP = 3
DIFFICULTY_STEP_FACTOR = 0.05

MAX_LIVES = 16
LIFE_LOSS = 1
MOLES_PER_LIFE = 2
LIVES_PER_MOLE = 1.1 * LIFE_LOSS / MOLES_PER_LIFE

STARTING_INTERVAL = 2 / MOLES_PER_LIFE
MINIMUM_INTERVAL = 0.1 * STARTING_INTERVAL

TRIGGER_SEQUENCE = ['A#', 'A', 'C', 'C', 'C']  # BACCC


class WhackAMole(Game):

    def __init__(self, led_controller: LEDController):
        super().__init__('WhackAMole', note_sequences=[TRIGGER_SEQUENCE], chord_sequences=[])
        self.lives = float(MAX_LIVES)
        self.score = 0
        self.tick_interval = float(STARTING_INTERVAL)
        self.moles: List[int] = []
        self.led_controller = led_controller
        self.thread: Optional[Thread] = None
        self.lock = Lock()

    def reset(self):
        self.lives = float(MAX_LIVES)
        self.score = 0
        self.tick_interval = float(STARTING_INTERVAL)
        self.moles: List[int] = []

    def trigger(self, note_sequence, chord_sequence):
        self.start()
        print('starting whackamole')

    def activate_note(self, full_note_name):
        position = get_position_from_full_note_name(full_note_name)
        self.try_to_whack_mole(position)

    def start(self):
        self.update_lives()
        self.thread = Thread(target=self.background_task)
        self.thread.start()
        print('started whackamole')

    def stop(self):
        self.finish()
        self.led_controller.show_failure_flash()
        self.reset()

    def update_lives(self):
        self.led_controller.set_range_to(
            get_full_note_name_from_position(0),
            get_full_note_name_from_position(math.floor(self.lives) - 1),
            Theme.active_color
        )
        time.sleep(0.001)
        if self.lives < MAX_LIVES:
            self.led_controller.set_range_to(
                get_full_note_name_from_position(math.ceil(self.lives)),
                get_full_note_name_from_position(START_INDEX - 1),
                Theme.inactive_color
            )

    def background_task(self):
        iterations = 0
        while self.is_running:
            time.sleep(self.tick_interval)
            if self.lock.acquire():
                if iterations == MOLES_PER_LIFE:
                    self.lives -= LIFE_LOSS
                    if self.lives <= 0:
                        # print('u ded')
                        self.stop()
                    else:
                        self.update_lives()
                    iterations = 0
                self.spawn_mole()
                self.lock.release()
                # print('lives:', self.lives)
            iterations += 1

    def spawn_mole(self):
        available_positions = [i for i in range(START_INDEX, END_INDEX) if i not in self.moles]
        if len(available_positions) == 0:
            return
        position = random.choice(available_positions)
        self.moles.append(position)
        self.led_controller.set_note_to(
            get_full_note_name_from_position(position),
            Theme.mole_color,
            'spawn mole on ' + str(position)
        )
        # print('spawned', position)

    def try_to_whack_mole(self, position):
        if position not in self.moles:
            # print(position, 'not whackable')
            return
        if self.lock.acquire():
            # print('whacked', position)
            self.moles.remove(position)
            self.score += 1
            # if self.score % SCORE_DIFFICULTY_STEP == 0 and self.tick_interval > MINIMUM_INTERVAL:
            #    self.tick_interval *= 1 - DIFFICULTY_STEP_FACTOR
            # if self.lives < MAX_LIVES - LIVES_PER_MOLE:
            #    self.lives += LIVES_PER_MOLE
            # self.lock.release()
