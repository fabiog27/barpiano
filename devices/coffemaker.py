import threading
import time

import gpiozero


class CoffeeMaker(object):

    def __init__(self, pin_number):
        self.coffees_poured = 0
        self.is_making_coffee = False
        self.pouring_duration = 20
        self.pin_number = pin_number

    def check(self, note_history):
        if len(note_history) < 4:
            return
        if ''.join(note_history[-4:]) == 'CAFE':
            if not self.is_making_coffee:
                self.is_making_coffee = True
                print('Making coffee...')
                coffee_thread = threading.Thread(target=self.make_coffee)
                coffee_thread.start()
            else:
                print('Can\'t make more than one coffee at a time!')

    def finish_coffee(self):
        self.coffees_poured += 1
        self.is_making_coffee = False
        print('Coffee is done')
        text = 'coffee poured' if self.coffees_poured == 1 else 'coffees poured'
        print(self.coffees_poured, text)

    def make_coffee(self):
        led = gpiozero.LED(self.pin_number)
        for i in range(self.pouring_duration):
            print('\r', end='')
            print('[' + (i + 1) * '*' + (self.pouring_duration - i - 1) * '-' + ']', end='')
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.5)
        print()
        self.finish_coffee()
