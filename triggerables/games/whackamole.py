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
DIFFICULTY_STEP_FACTOR = 0.3

MAX_LIVES = 16
LIFE_LOSS = 1
LIVES_PER_MOLE = 1.1 * LIFE_LOSS / 6

MOLES_PER_LIFE = 6
STARTING_INTERVAL = 1 / MOLES_PER_LIFE
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
        if self.thread is not None:
            self.thread.join()
            self.thread = None
        self.finish()
        self.led_controller.show_failure_flash()
        self.reset()

    def update_lives(self):
        for i in range(16):
            color = Theme.active_color
            if i > self.lives:
                color = Theme.inactive_color
            self.led_controller.set_note_to(get_full_note_name_from_position(i), color)

    def background_task(self):
        iterations = 0
        while self.is_running:
            time.sleep(self.tick_interval)
            if self.lock.acquire(blocking=False):
                if iterations == MOLES_PER_LIFE:
                    self.lives -= LIFE_LOSS
                    iterations = 0
                self.spawn_mole()
                self.lock.release()
                print('lives:', self.lives)
                self.update_lives()
            if self.lives <= 0:
                print('u ded')
                self.stop()

    def spawn_mole(self):
        position = random.randint(START_INDEX, END_INDEX)
        while position in self.moles:
            position = random.randint(START_INDEX, END_INDEX)
        self.moles.append(position)
        self.led_controller.set_note_to(get_full_note_name_from_position(position), Theme.mole_color)
        print('spawned', position)

    def try_to_whack_mole(self, position):
        if position not in self.moles:
            print(position, 'not whackable')
            return
        if self.lock.acquire():
            print('whacked', position)
            self.moles.remove(position)
            self.score += 1
            if self.score % SCORE_DIFFICULTY_STEP == 0 and self.tick_interval > MINIMUM_INTERVAL:
                self.tick_interval *= 1 - DIFFICULTY_STEP_FACTOR
            if self.lives < MAX_LIVES - LIVES_PER_MOLE:
                self.lives += LIVES_PER_MOLE
            self.lock.release()
