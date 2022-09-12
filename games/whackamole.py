import random
import time
from threading import Thread, Lock
from typing import List, Optional

from constants.colors import MOLE, ACTIVE_GREEN, MELLOW_WHITE
from controllers.led_controller import LEDController
from devices.device import Device
from helpers.notes import get_full_note_name_from_position

MIN_PLAYABLE = 'E2'
MAX_PLAYABLE = 'F7'

START_INDEX = 16
END_INDEX = 77

MAX_LIVES = 16

TRIGGER_SEQUENCE = ['A#', 'A', 'C', 'C', 'C']  # BACCC


class WhackAMole(Device):

    def __init__(self, led_controller: LEDController):
        super().__init__('WhackAMole', note_sequences=[TRIGGER_SEQUENCE], chord_sequences=[])
        self.lives = MAX_LIVES
        self.score = 0
        self.life_interval = 1
        self.mole_interval = 1
        self.moles: List[int] = []
        self.led_controller = led_controller
        self.thread: Optional[Thread] = None
        self.lock = Lock()

    def trigger(self, note_sequence, chord_sequence):
        self.start()
        print('starting whackamole')

    def start(self):
        self.update_lives()
        self.thread = Thread(target=self.background_task)
        self.thread.start()
        print('started whackamole')

    def stop(self):
        self.thread = None
        self.finish()
        self.led_controller.show_failure_flash()

    def update_lives(self):
        for i in range(16):
            color = ACTIVE_GREEN
            if i >= self.lives:
                color = MELLOW_WHITE
            self.led_controller.set_note_to(get_full_note_name_from_position(i), color)

    def background_task(self):
        should_spawn_mole = True
        while self.is_running:
            print('background task')
            time.sleep(self.life_interval)
            if self.lock.acquire(blocking=False):
                self.lives -= 1
                if should_spawn_mole:
                    self.spawn_mole()
                    should_spawn_mole = False
                else:
                    should_spawn_mole = True
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
        self.led_controller.set_note_to(get_full_note_name_from_position(position), MOLE)
        print('spawned', position)

    def try_to_whack_mole(self, position):
        if position not in self.moles:
            print(position, 'not whackable')
            return
        if self.lock.acquire():
            print('whacked', position)
            self.moles.remove(position)
            self.score += 1
            if self.score % 10 == 0 and self.life_interval > 0.1:
                self.life_interval -= 0.1
                self.mole_interval += 0.05
            if self.lives < 15:
                self.lives += 2
            self.lock.release()
