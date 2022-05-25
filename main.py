from controller import Controller
from devices.coffeemaker import CoffeeMaker
from midimon import midimon

COFFEE_ARDUINO_IDENTIFIER = '/dev/ttyACM0'

if __name__ == '__main__':
    coffee_maker = CoffeeMaker(
        serial_identifier=COFFEE_ARDUINO_IDENTIFIER,
    )
    controller = Controller()
    controller.add_device(coffee_maker)
    midimon.register_controller(controller)
    midimon.start_monitor()
