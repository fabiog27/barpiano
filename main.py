from controllers.history_controller import HistoryController
from controllers.single_note_controller import SingleNoteController
from devices.coffeemaker import CoffeeMaker
from controllers.led_controller import LEDController
from devices.lock import Lock
from games.whackamole import WhackAMole
from midimon import midimon

COFFEE_ARDUINO_IDENTIFIER = '/dev/ttyUSB0'
# COFFEE_ARDUINO_IDENTIFIER = '/dev/'
LED_ARDUINO_IDENTIFIER = '/dev/ttyUSB1'
# LED_ARDUINO_IDENTIFIER = '/dev/cu.usbserial-143230'

if __name__ == '__main__':
    coffee_maker = CoffeeMaker(
        serial_identifier=COFFEE_ARDUINO_IDENTIFIER,
    )
    lock = Lock()
    led_controller = LEDController(
        serial_identifier=LED_ARDUINO_IDENTIFIER,
    )
    whack_a_mole = WhackAMole(led_controller)
    controller = HistoryController()
    controller.add_device(whack_a_mole)
    controller.add_device(coffee_maker)
    controller.add_device(lock)
    midimon.register_controller(controller)
    single_note_controller = SingleNoteController(whack_a_mole)
    coffee_maker.set_led_controller(led_controller)
    midimon.register_led_controller(led_controller)
    midimon.register_single_note_controller(single_note_controller)
    midimon.start_monitor()
