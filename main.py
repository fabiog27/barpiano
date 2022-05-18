from devices.coffemaker import CoffeeMaker
from devices.watercooker import WaterCooker
from midimon import midimon

COFFEE_GPIO_PIN = 17
WATER_GPIO_PIN = 27

if __name__ == '__main__':
    coffee_maker = CoffeeMaker(COFFEE_GPIO_PIN)
    water_cooker = WaterCooker(WATER_GPIO_PIN, 20, 'DEsCB')
    midimon.register_observer(coffee_maker, 4)
    midimon.register_observer(water_cooker, 4)
    midimon.start_monitor()
