from queue import Queue, Empty
from threading import Thread
from typing import cast, Optional, Tuple

import serial

from constants.colors import COLORS
from constants.leds import LEDS
from helpers.serial_connection import send_arduino_message
from ledcontroller.typed_queue import TypedQueue


class LEDMessage(object):

    def __init__(self, starting_led: int, ending_led: int, color: Tuple[int, int, int], purpose=''):
        self.starting_led = starting_led
        self.ending_led = ending_led
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        self.purpose = purpose

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
        self.serial_identifier = serial_identifier

    def add_message(self, message: LEDMessage):
        self.queue.put(message, timeout=1)

    def work_messages(self):
        serial_connection = None
        if self.serial_identifier != 'unknown':
            serial_connection = serial.Serial(self.serial_identifier, baudrate=921600, timeout=0.1)
        led_message = None
        while self.is_running:
            if serial_connection is None:
                try:
                    print('waiting for led message')
                    led_message = self.queue.get(timeout=10)
                except Empty:
                    continue
                print('message purpose:', led_message.purpose)
                self.queue.task_done()
                continue
            try:
                has_waited = False
                while serial_connection.out_waiting > 0:
                    print('output waiting')
                    has_waited = True
                if has_waited and led_message is not None:
                    print(led_message.purpose)
                led_message = self.queue.get(timeout=10)
                encoded_message = led_message.build_message().encode('ascii')
                serial_connection.write(encoded_message)
                self.queue.task_done()
            except Empty:
                pass
        if serial_connection is not None:
            serial_connection.close()

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
