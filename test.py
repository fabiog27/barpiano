import time

from triggerables.devices.coffeemaker import CoffeeMaker, COFFEE_1_SEQUENCE

COFFEE_GPIO_PIN = 17
COFFEE_ARDUINO_IDENTIFIER = '/dev/ttyUSB0'

coffee_maker = CoffeeMaker(
    serial_identifier=COFFEE_ARDUINO_IDENTIFIER,
)

if __name__ == '__main__':
    time.sleep(3)
    # coffee_maker.start_up()
    coffee_maker.trigger(COFFEE_1_SEQUENCE, [])
