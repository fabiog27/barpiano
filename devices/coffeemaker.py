import time
import serial
import gpiozero

from typing import List, Optional

from devices.device import Device
from devices.ledcontroller import LEDController
from helpers.serial_connection import send_arduino_message

POWER_SEQUENCE = ['A', 'C', 'D', 'C']  # DUH
CLEAN_SEQUENCE = ['A#', 'A', 'C', 'B']  # BACH
COFFEE_1_SEQUENCE = ['C', 'A', 'F', 'E']  # DUH
COFFEE_2_SEQUENCE = [['C', 'C'], ['A', 'A'], ['F', 'F'], ['E', 'E']]  # DUH
ESPRESSO_1_SEQUENCE = ['E', 'D#', 'A#', 'E', 'D#', 'D#']  # Esb(r)ess(o)
ESPRESSO_2_SEQUENCE = [['E', 'E'], ['D#', 'D#'], ['A#', 'A#'], ['E', 'E'], ['D#', 'D#'], ['D#', 'D#']]  # Double that
STEAM_SEQUENCE = ['D', 'D#', 'C', 'B']  # DSCH


class CoffeeMaker(Device):
    POWER_BUTTON_PIN = 17
    ESPRESSO_BUTTON_PIN = 27
    DOUBLE_ESPRESSO_BUTTON_PIN = 22
    CLEAN_BUTTON_PIN = 5
    DOUBLE_COFFEE_BUTTON_PIN = 6
    COFFEE_BUTTON_PIN = 13
    STEAM_BUTTON_PIN = 12

    POWER_ACTION = 'power'
    ESPRESSO_ACTION = 'espresso'
    DOUBLE_ESPRESSO_ACTION = 'doubleEspresso'
    CLEAN_ACTION = 'clean'
    DOUBLE_COFFEE_ACTION = 'doubleCoffee'
    COFFEE_ACTION = 'coffee'
    STEAM_ACTION = 'steam'

    WAIT_TIME = 30

    def __init__(self, serial_identifier: str):
        super().__init__(
            'Coffee Maker',
            note_sequences=[
                POWER_SEQUENCE,
                ESPRESSO_1_SEQUENCE,
                CLEAN_SEQUENCE,
                COFFEE_1_SEQUENCE,
                STEAM_SEQUENCE,
            ],
            chord_sequences=[ESPRESSO_2_SEQUENCE, COFFEE_2_SEQUENCE]
        )
        self.led_controller: Optional[LEDController] = None

        self.serial_connection = serial.Serial(serial_identifier, baudrate=9600, timeout=0.5)
        self.power_button = gpiozero.Button(self.POWER_BUTTON_PIN)
        self.espresso_button = gpiozero.Button(self.ESPRESSO_BUTTON_PIN)
        self.double_espresso_button = gpiozero.Button(self.DOUBLE_ESPRESSO_BUTTON_PIN)
        self.clean_button = gpiozero.Button(self.CLEAN_BUTTON_PIN)
        self.double_coffee_button = gpiozero.Button(self.DOUBLE_COFFEE_BUTTON_PIN)
        self.coffee_button = gpiozero.Button(self.COFFEE_BUTTON_PIN)
        self.steam_button = gpiozero.Button(self.STEAM_BUTTON_PIN)

        self.power_button.when_released = lambda: send_arduino_message(self.serial_connection, self.POWER_ACTION)
        self.espresso_button.when_released = lambda: send_arduino_message(self.serial_connection, self.ESPRESSO_ACTION)
        self.double_espresso_button.when_released = lambda: send_arduino_message(
            self.serial_connection,
            self.DOUBLE_ESPRESSO_ACTION
        )
        self.clean_button.when_released = lambda: send_arduino_message(self.serial_connection, self.CLEAN_ACTION)
        self.double_coffee_button.when_released = lambda: send_arduino_message(
            self.serial_connection,
            self.DOUBLE_COFFEE_ACTION
        )
        self.coffee_button.when_released = lambda: send_arduino_message(self.serial_connection, self.COFFEE_ACTION)
        self.steam_button.when_released = lambda: send_arduino_message(self.serial_connection, self.STEAM_ACTION)

    def set_led_controller(self, led_controller: LEDController):
        self.led_controller = led_controller

    def trigger(self, note_sequence: List[str], chord_sequence: List[List[str]]) -> None:
        action = None
        if note_sequence == POWER_SEQUENCE:
            action = CoffeeMaker.POWER_ACTION
            print('POWER')
        elif note_sequence == ESPRESSO_1_SEQUENCE:
            action = CoffeeMaker.ESPRESSO_ACTION
            print('ESPRESSO_1_SEQUENCE')
        elif chord_sequence == ESPRESSO_2_SEQUENCE:
            action = CoffeeMaker.DOUBLE_ESPRESSO_ACTION
            print('ESPRESSO_2_SEQUENCE')
        elif note_sequence == CLEAN_SEQUENCE:
            action = CoffeeMaker.CLEAN_ACTION
            print('CLEAN_SEQUENCE')
        elif note_sequence == COFFEE_1_SEQUENCE:
            action = CoffeeMaker.COFFEE_ACTION
            print('COFFEE_1_SEQUENCE')
        elif chord_sequence == COFFEE_2_SEQUENCE:
            action = CoffeeMaker.DOUBLE_COFFEE_ACTION
            print('COFFEE_2_SEQUENCE')
        elif note_sequence == STEAM_SEQUENCE:
            action = CoffeeMaker.STEAM_ACTION
            print('STEAM_SEQUENCE')
        if action is not None:
            try:
                message = '{"action":"' + action + '"}'
                send_arduino_message(self.serial_connection, message)
                if self.led_controller is not None:
                    self.led_controller.show_success_flash()
                    self.led_controller.show_loading_sequence(CoffeeMaker.WAIT_TIME)
            except RuntimeError:
                self.finish()
                return
            time.sleep(CoffeeMaker.WAIT_TIME)
        self.finish()

    def start_up(self) -> bool:
        try:
            send_arduino_message(self.serial_connection, CoffeeMaker.POWER_ACTION)
            return True
        except RuntimeError:
            return False

    def shut_down(self) -> bool:
        try:
            send_arduino_message(self.serial_connection, CoffeeMaker.POWER_ACTION)
            return True
        except RuntimeError:
            return False
