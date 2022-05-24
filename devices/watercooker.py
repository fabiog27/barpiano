import time
import gpiozero

from typing import List

import serial

from devices.device import Device


class WaterCooker(Device):

    def __init__(self, gpio_pin_number: int, serial_identifier: str, duration: int, note_sequence: List[str]):
        super().__init__('Water Cooker', gpio_pin_number, duration, note_sequence)
        self.serial_connection = serial.Serial(serial_identifier, baudrate=9600, timeout=0.5)

    def trigger(self) -> None:
        led = gpiozero.LED(self.pin_number)
        for i in range(self.duration):
            print('\r', end='')
            print('[' + (i + 1) * '*' + (self.duration - i - 1) * '-' + ']', end='')
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.5)
        print()
        self.finish()
