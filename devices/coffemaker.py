import time
import gpiozero

from typing import List

from devices.device import Device


class CoffeeMaker(Device):

    def __init__(self, gpio_pin_number: int, duration: int, note_sequence: List[str]):
        super().__init__('Coffee Maker', gpio_pin_number, duration, note_sequence)

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
