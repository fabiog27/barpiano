import threading
import time

import gpiozero


class WaterCooker(object):

    def __init__(self, pin_number, cooking_duration, trigger):
        self.waters_cooked = 0
        self.is_cooking = False
        self.cooking_duration = cooking_duration
        self.pin_number = pin_number
        self.trigger = trigger

    def check(self, note_history):
        if len(note_history) < len(self.trigger):
            return
        print(''.join(note_history[-len(self.trigger):]))
        print(self.trigger)
        if ''.join(note_history[-len(self.trigger):]) == self.trigger:
            if not self.is_cooking:
                self.is_cooking = True
                print('Heating water...')
                tea_thread = threading.Thread(target=self.cook_water)
                tea_thread.start()
            else:
                print('Can\'t heat more than one water at a time!')

    def finish_cooking(self):
        self.waters_cooked += 1
        self.is_cooking = False
        print('Water is hot')
        text = 'water heated' if self.waters_cooked == 1 else 'waters heated'
        print(self.waters_cooked, text)

    def cook_water(self):
        led = gpiozero.LED(self.pin_number)
        for i in range(self.cooking_duration):
            print('\r', end='')
            print('[' + (i + 1) * '*' + (self.cooking_duration - i - 1) * '-' + ']', end='')
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.5)
        print()
        self.finish_cooking()
