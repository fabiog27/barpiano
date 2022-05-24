import time
import serial

from typing import List

from devices.device import Device

COFFEE_MAKER_ARDUINO_IDENTIFIER = '/dev/ttyACM0'


class CoffeeMaker(Device):

    def __init__(self, gpio_pin_number: int, serial_identifier: str, duration: int, note_sequence: List[str]):
        super().__init__('Coffee Maker', gpio_pin_number, duration, note_sequence)
        self.serial_connection = serial.Serial(serial_identifier, baudrate=9600, timeout=0.5)

    def trigger(self) -> None:
        message = '{"coffeeType":"c","coffeeAmount":1}'.encode('ascii')
        self.serial_connection.write(message)
        response_part = self.serial_connection.readline().decode('ascii')
        response = response_part
        response_part = self.serial_connection.readline().decode('ascii')
        while response_part != '':
            response += response_part
            response_part = self.serial_connection.readline().decode('utf-8')
        if response != '1\r\n':
            print('Can\'t make coffee:\n', response)
            self.finish()
            return
        self.wait()
        self.finish()
