from midi import midimon
import gpiozero
import time
import threading


class CoffeeMaker(object):

    def __init__(self):
        self.coffees_poured = 0
        self.is_making_coffee = False
        self.pouring_duration = 20

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
        green_led = gpiozero.LED(17)
        red_led = gpiozero.LED(27)
        for i in range(self.pouring_duration):
            print('\r', end='')
            print('[' + (i + 1) * '*' + (self.pouring_duration - i - 1) * '-' + ']', end='')
            green_led.on()
            red_led.off()
            time.sleep(0.5)
            green_led.off()
            red_led.on()
            time.sleep(0.5)
        print()
        self.finish_coffee()


if __name__ == '__main__':
    coffee_maker = CoffeeMaker()
    midimon.register_observer(coffee_maker, 4)
    midimon.start_monitor()
