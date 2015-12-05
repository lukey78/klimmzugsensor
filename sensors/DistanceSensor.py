__author__ = 'Jens'

import time
from datetime import datetime


class DistanceSensor:

    def __init__(self, wiringpi, pin_echo, pin_trig):
        self.wiringpi = wiringpi
        self.pin_echo = pin_echo
        self.pin_trig = pin_trig

        self.wiringpi.pinMode(self.pin_echo, 0)
        self.wiringpi.pinMode(self.pin_trig, 1)

    def _delay(self, delay_microseconds):
        time.sleep(delay_microseconds/1000000.0)

    def measure(self):
        tv1 = 0
        tv2 = 0
        start = 0
        stop = 0
        distance = 0
        millisStart = 0

        self.wiringpi.digitalWrite(self.pin_trig, 0)
        self._delay(10)

        self.wiringpi.digitalWrite(self.pin_trig, 1)
        self._delay(5)
        self.wiringpi.digitalWrite(self.pin_trig, 0)

        millisStart = self.wiringpi.millis()
        while not self.wiringpi.digitalRead(self.pin_echo) == 1:
            if self.wiringpi.millis() > millisStart + 1000:
                return -1

        tv1 = datetime.now()

        millisStart = self.wiringpi.millis()
        while not self.wiringpi.digitalRead(self.pin_echo) == 0:
            if self.wiringpi.millis() > millisStart + 1000:
                return -1

        tv2 = datetime.now()

        start = tv1.second * 1000000 + tv1.microsecond
        stop = tv2.second * 1000000 + tv2.microsecond
        distance = float(stop - start) / 1000000.0 * 34000.0 / 2.0

        return distance
