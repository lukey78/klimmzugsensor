__author__ = 'Jens'

from libs.lcd1602 import Adafruit_CharLCD


class Display:

    def __init__(self, pin_rs, pin_e, pin_d4, pin_d5, pin_d6, pin_d7, pin_grnd = -1):
        self.has_grnd = pin_grnd
        self.lcd = Adafruit_CharLCD(pin_rs, pin_e, [pin_d4, pin_d5, pin_d6, pin_d7], None, pin_grnd)
        self.lcd.backlight_on()
        self.lcd.begin(16, 2)
        self.lcd.clear()

    def on(self):
        if self.has_grnd >= 0:
            self.lcd.backlight_on()
        self.lcd.clear()

    def off(self):
        self.lcd.clear()
        if self.has_grnd >= 0:
            self.lcd.backlight_off()

    def message(self, col, row, message):
        self.lcd.setCursor(col, row)
        self.lcd.message(message)

    def clear(self):
        self.lcd.clear()

    def clear_row(self, row):
        self.message(0, row, "                ")
