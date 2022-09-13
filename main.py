from notecontrollers.history_controller import HistoryController
from notecontrollers.single_note_controller import SingleNoteController
from triggerables.devices.coffeemaker import CoffeeMaker
from ledcontroller.led_controller import LEDController
from triggerables.devices.lock import Lock
from triggerables.games.whackamole import WhackAMole
from midimon import midimon

COFFEE_ARDUINO_IDENTIFIER = '/dev/ttyUSB0'
# COFFEE_ARDUINO_IDENTIFIER = '/dev/'
LED_ARDUINO_IDENTIFIER = '/dev/ttyUSB1'
# LED_ARDUINO_IDENTIFIER = '/dev/cu.usbserial-143230'

if __name__ == '__main__':
    # Init controllers
    controller = HistoryController()
    led_controller = LEDController(
        serial_identifier=LED_ARDUINO_IDENTIFIER,
    )
    single_note_controller = SingleNoteController(led_controller)

    # Init triggerables
    coffee_maker = CoffeeMaker(
        serial_identifier=COFFEE_ARDUINO_IDENTIFIER,
        led_controller=led_controller
    )
    controller.add_triggerable(coffee_maker)
    lock = Lock()
    controller.add_triggerable(lock)
    whack_a_mole = WhackAMole(led_controller)
    controller.add_triggerable(whack_a_mole)
    single_note_controller.add_game(whack_a_mole)

    midimon.register_controller(controller)
    midimon.register_single_note_controller(single_note_controller)
    midimon.start_monitor()
