import time
import serial

from typing import List

from devices.device import Device

COFFEE_1_SEQUENCE = ['C', 'A', 'F', 'E']


class CoffeeMaker(Device):

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
        message = ('{"action":"' + CoffeeMaker.POWER_ACTION + '"}').encode('ascii')
        try:
            self.trigger_arduino(message)
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
