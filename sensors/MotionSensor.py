__author__ = 'Jens'

class MotionSensor:

    def __init__(self, wiringpi, motion_sensor_pin, function_to_trigger = None):
        self.motion_sensor_pin = motion_sensor_pin
        self.wiringpi = wiringpi
        self.function_to_trigger = function_to_trigger
        self.wiringpi.pinMode(self.motion_sensor_pin, 0)

    def sense(self):
        # senses motion and returns 1 for "motion detected" or 0 for "no motion"
        if self.wiringpi.digitalRead(self.motion_sensor_pin) == 1:
            if self.function_to_trigger:
                self.function_to_trigger()
            return 1

        return 0

