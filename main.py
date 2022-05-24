from controller import Controller
from devices.coffemaker import CoffeeMaker
from devices.watercooker import WaterCooker
from midimon import midimon

COFFEE_GPIO_PIN = 17
COFFEE_ARDUINO_IDENTIFIER = '/dev/ttyACM0'
WATER_GPIO_PIN = 27
WATER_ARDUINO_IDENTIFIER = '/dev/ttyACM1'  # TODO: TBD

if __name__ == '__main__':
    coffee_maker = CoffeeMaker(
        gpio_pin_number=COFFEE_GPIO_PIN,
        serial_identifier=COFFEE_ARDUINO_IDENTIFIER,
        duration=20,
        note_sequence=['C', 'A', 'F', 'E'],
    )
    water_cooker = WaterCooker(
        gpio_pin_number=WATER_GPIO_PIN,
        serial_identifier=WATER_ARDUINO_IDENTIFIER,
        duration=20,
        note_sequence=['D', 'D#', 'C', 'B'],
    )
    controller = Controller()
    controller.add_device(coffee_maker)
    controller.add_device(water_cooker)
    midimon.register_controller(controller)
    midimon.start_monitor()
