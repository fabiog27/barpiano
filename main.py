import subprocess
import serial
from typing import List

from notecontrollers.history_controller import HistoryController
from notecontrollers.single_note_controller import SingleNoteController
from triggerables.devices.coffeemaker import CoffeeMaker
from ledcontroller.led_controller import LEDController
from triggerables.devices.lock import Lock
from triggerables.games.whackamole import WhackAMole
from midimon import midimon

COFFEE_ARDUINO_FUNCTION = 'coffee-maker'
LED_ARDUINO_FUNCTION = 'led-controller'

BAUD_RATES = [9600, 921600]


def get_usb_devices() -> List[str]:
    ls_output = subprocess.check_output(['ls', '/dev']).decode('ascii')
    devices = ls_output.split('\n')
    usb_device_list = ['/dev/' + device for device in devices if 'ttyUSB' in device]
    print('Detected USB devices:')
    print(usb_device_list)
    return usb_device_list


def find_device_identifier_by_function(usb_device_list: List[str], function: str) -> str:
    for device in usb_device_list:
        try:
            for baud_rate in BAUD_RATES:
                try:
                    ser = serial.Serial(device, baudrate=baud_rate, timeout=0.5)
                    ser.write(b'Aget device funcZ')
                    response = ser.readline().decode('ascii')
                    if function in response:
                        ser.close()
                        return device
                except UnicodeDecodeError:
                    continue
        except serial.SerialException or serial.SerialTimeoutException:
            continue
    raise ValueError('Device ' + function + ' not found')


if __name__ == '__main__':
    # Find USB devices
    usb_devices = get_usb_devices()
    led_controller_serial_identifier = find_device_identifier_by_function(usb_devices, LED_ARDUINO_FUNCTION)
    coffee_maker_serial_identifier = find_device_identifier_by_function(usb_devices, COFFEE_ARDUINO_FUNCTION)

    # Init controllers
    controller = HistoryController()
    led_controller = LEDController(
        serial_identifier=led_controller_serial_identifier,
    )
    single_note_controller = SingleNoteController(led_controller)

    # Init triggerables
    coffee_maker = CoffeeMaker(
        serial_identifier=coffee_maker_serial_identifier,
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
