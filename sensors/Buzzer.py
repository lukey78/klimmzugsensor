__author__ = 'Jens'

import time


class Buzzer:

    def __init__(self, wiringpi, buzzer_pin):
        self.wiringpi = wiringpi
        self.buzzer_pin = buzzer_pin

        self.wiringpi.pinMode(self.buzzer_pin, 1)
        self.wiringpi.digitalWrite(self.buzzer_pin, 1)

    def _delay(self, delay_microseconds):
        time.sleep(delay_microseconds/1000000.0)

    def beep(self, microseconds):
        self.wiringpi.digitalWrite(self.buzzer_pin, 0)
        self._delay(microseconds)
        self.wiringpi.digitalWrite(self.buzzer_pin, 1)
