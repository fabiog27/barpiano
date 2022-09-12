import time

from controller import Controller
from devices.coffeemaker import CoffeeMaker
from devices.ledcontroller import LEDController
from devices.lock import Lock
from midimon import midimon

COFFEE_ARDUINO_IDENTIFIER = '/dev/ttyUSB0'
LED_ARDUINO_IDENTIFIER = '/dev/ttyUSB1'

if __name__ == '__main__':
    coffee_maker = CoffeeMaker(
        serial_identifier=COFFEE_ARDUINO_IDENTIFIER,
    )
    lock = Lock()
    controller = Controller()
    controller.add_device(coffee_maker)
    controller.add_device(lock)
    midimon.register_controller(controller)
    led_controller = LEDController(
        serial_identifier=LED_ARDUINO_IDENTIFIER,
    )
    coffee_maker.set_led_controller(led_controller)
    midimon.register_led_controller(led_controller)
    midimon.start_monitor()
