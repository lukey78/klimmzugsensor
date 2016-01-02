__author__ = 'Jens'


class Led:

    def __init__(self, wiringpi, led_pin):
        self.wiringpi = wiringpi
        self.led_pin = led_pin

        self.wiringpi.pinMode(self.led_pin, 1)

    def control(self, state):
        self.wiringpi.digitalWrite(self.led_pin, state)

    def on(self):
        self.control(1)

    def off(self):
        self.control(0)

