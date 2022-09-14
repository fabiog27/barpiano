from queue import Queue, Empty
from threading import Thread
from typing import cast, Optional, Tuple

import serial

from constants.colors import COLORS
from constants.leds import LEDS
from helpers.serial_connection import send_arduino_message
from ledcontroller.typed_queue import TypedQueue


class LEDMessage(object):

    def __init__(self, starting_led: int, ending_led: int, color: Tuple[int, int, int]):
        self.starting_led = starting_led
        self.ending_led = ending_led
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]

    def build_message(self):
        return 'A{:03d}{:03d}{:03d}{:03d}{:03d}ZX'.format(self.starting_led, self.ending_led, self.r, self.g, self.b)

    @staticmethod
    def get_reset_message():
        return LEDMessage(0, LEDS.PIXEL_AMOUNT - 1, COLORS.BLACK).build_message()


LEDMessageQueue = TypedQueue[LEDMessage]


class LEDMessageManager(object):

    def __init__(self, serial_identifier: str):
        self.queue = cast(LEDMessageQueue, Queue())
        self.worker_thread: Optional[Thread] = None
        self.is_running = False
        self.serial_connection = serial.Serial(serial_identifier, baudrate=921600, timeout=0.001)

    def add_message(self, message: LEDMessage):
        self.queue.put(message, block=False)

    def work_messages(self):
        while self.is_running:
            try:
                led_message = self.queue.get(timeout=10)
                send_arduino_message(self.serial_connection, led_message.build_message())
                self.queue.task_done()
            except Empty:
                pass

    def start(self):
        self.is_running = True
        self.worker_thread = Thread(target=self.work_messages)
        self.worker_thread.start()

    def stop(self):
        self.is_running = False
        self.queue.empty()
        if self.worker_thread is not None:
            self.worker_thread.join()
            self.worker_thread = None
        send_arduino_message(self.serial_connection, LEDMessage.get_reset_message())
