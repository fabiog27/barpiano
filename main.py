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
    midimon.register_observer(coffee_maker, 4)
    midimon.register_observer(water_cooker, 4)
    midimon.start_monitor()
