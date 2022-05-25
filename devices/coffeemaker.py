import time
import serial
import gpiozero

from typing import List

from devices.device import Device

COFFEE_1_SEQUENCE = ['C', 'A', 'F', 'E']


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

    POWER_TIME = 70
    ESPRESSO_TIME = 60
    DOUBLE_ESPRESSO_TIME = 60
    CLEAN_TIME = 60
    DOUBLE_COFFEE_TIME = 60
    COFFEE_TIME = 60
    STEAM_TIME = 60

    def __init__(self, serial_identifier: str):
        super().__init__('Coffee Maker', note_sequences=[COFFEE_1_SEQUENCE], chord_sequences=[])
        self.serial_connection = serial.Serial(serial_identifier, baudrate=9600, timeout=0.5)
        self.power_button = gpiozero.Button(self.POWER_BUTTON_PIN)
        self.espresso_button = gpiozero.Button(self.ESPRESSO_BUTTON_PIN)
        self.double_espresso_button = gpiozero.Button(self.DOUBLE_ESPRESSO_BUTTON_PIN)
        self.clean_button = gpiozero.Button(self.CLEAN_BUTTON_PIN)
        self.double_coffee_button = gpiozero.Button(self.DOUBLE_COFFEE_BUTTON_PIN)
        self.coffee_button = gpiozero.Button(self.COFFEE_BUTTON_PIN)
        self.steam_button = gpiozero.Button(self.STEAM_BUTTON_PIN)

        self.power_button.when_released = lambda: self.trigger_arduino(self.POWER_ACTION)
        self.espresso_button.when_released = lambda: self.trigger_arduino(self.ESPRESSO_ACTION)
        self.double_espresso_button.when_released = lambda: self.trigger_arduino(self.DOUBLE_ESPRESSO_ACTION)
        self.clean_button.when_released = lambda: self.trigger_arduino(self.CLEAN_ACTION)
        self.double_coffee_button.when_released = lambda: self.trigger_arduino(self.DOUBLE_COFFEE_ACTION)
        self.coffee_button.when_released = lambda: self.trigger_arduino(self.COFFEE_ACTION)
        self.steam_button.when_released = lambda: self.trigger_arduino(self.STEAM_ACTION)

    def trigger(self, note_sequence: List[str], chord_sequence: List[List[str]]) -> None:
        action = None
        wait_time = None
        if note_sequence == COFFEE_1_SEQUENCE:
            action = CoffeeMaker.COFFEE_ACTION
            wait_time = CoffeeMaker.COFFEE_TIME
        if action is not None and wait_time is not None:
            try:
                self.trigger_arduino(action)
            except RuntimeError:
                self.finish()
                return
            time.sleep(wait_time)
        self.finish()

    def start_up(self) -> bool:
        try:
            self.trigger_arduino(CoffeeMaker.POWER_ACTION)
            time.sleep(CoffeeMaker.POWER_TIME)
            return True
        except RuntimeError:
            return False

    def shut_down(self) -> bool:
        try:
            self.trigger_arduino(CoffeeMaker.POWER_ACTION)
            time.sleep(CoffeeMaker.POWER_TIME)
            return True
        except RuntimeError:
            return False

    def trigger_arduino(self, action):
        message = ('{"action":"' + action + '"}').encode('ascii')
        self.serial_connection.write(message)
        response_part = self.serial_connection.readline().decode('ascii')
        response = response_part
        response_part = self.serial_connection.readline().decode('ascii')
        while response_part != '':
            response += response_part
            response_part = self.serial_connection.readline().decode('ascii')
        if 'Error' in response:
            raise RuntimeError('Can\'t run coffee machine:\n' + response)
