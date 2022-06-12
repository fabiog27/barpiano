from controller import Controller
from devices.coffeemaker import CoffeeMaker
from devices.lock import Lock
from midimon import midimon

COFFEE_ARDUINO_IDENTIFIER = '/dev/ttyUSB0'

if __name__ == '__main__':
    coffee_maker = CoffeeMaker(
        serial_identifier=COFFEE_ARDUINO_IDENTIFIER,
    )
    lock = Lock()
    controller = Controller()
    controller.add_device(coffee_maker)
    controller.add_device(lock)
    midimon.register_controller(controller)
    midimon.start_monitor()
