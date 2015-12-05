__author__ = 'Jens'
from datetime import datetime


class InactivityTimer:

    def __init__(self, activation_function, deactivation_function, delay):
        self.activation_function = activation_function
        self.deactivation_function = deactivation_function
        self.delay = delay
        self.last_wakeup_trigger = 0
        self.active = 0

    def _get_curtime(self):
        now = datetime.now()
        curtime = now.hour * 3600 + now.minute * 60 + now.second
        return curtime

    def trigger(self):
        self.last_wakeup_trigger = self._get_curtime()

    def loop(self):
        curtime = self._get_curtime()

        if self.active == 0 and self.last_wakeup_trigger >= curtime:
            self.activation_function()
            self.active = 1

        elif self.active == 1 and curtime > (self.last_wakeup_trigger + self.delay):
            self.deactivation_function()
            self.active = 0

    def is_active(self):
        return self.active

    def get_seconds_till_shutdown(self):
        return str(self.delay - (self._get_curtime() - self.last_wakeup_trigger))

