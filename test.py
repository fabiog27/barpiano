import time

from devices.coffemaker import CoffeeMaker

COFFEE_GPIO_PIN = 17
COFFEE_ARDUINO_IDENTIFIER = '/dev/cu.usbmodem1422401'

coffee_maker = CoffeeMaker(
    gpio_pin_number=COFFEE_GPIO_PIN,
    serial_identifier=COFFEE_ARDUINO_IDENTIFIER,
    duration=20,
    note_sequence=['C', 'A', 'F', 'E'],
)

if __name__ == '__main__':
    time.sleep(3)
    coffee_maker.trigger()
