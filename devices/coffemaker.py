import time
import serial

from typing import List

from devices.device import Device

COFFEE_MAKER_ARDUINO_IDENTIFIER = '/dev/ttyACM0'


class CoffeeMaker(Device):

    def __init__(self, gpio_pin_number: int, duration: int, note_sequence: List[str]):
        super().__init__('Coffee Maker', gpio_pin_number, duration, note_sequence)

    def trigger(self) -> None:
        arduino_connection = serial.Serial(COFFEE_MAKER_ARDUINO_IDENTIFIER, 9600, timeout=.1)
        arduino_connection.write(b'c,0,1')
        time.sleep(1)
        response_part = arduino_connection.read().decode('utf-8')
        response = response_part
        while response_part != '':
            response_part = arduino_connection.read().decode('utf-8')
            response += response_part
        if response != '1':
            print('Can\'t make coffee:\n', response)
            self.finish()
            return
        self.wait()
        self.finish()
