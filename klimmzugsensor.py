#!/usr/bin/env/python

import time

import wiringpi2 as wiringpi
from helper.InactivityTimer import InactivityTimer
from sensors.MotionSensor import MotionSensor
from sensors.DistanceSensor import DistanceSensor
from sensors.Display import Display
from sensors.Buzzer import Buzzer
from sensors.Led import Led

DEBUG = 1

# Globals
INPUT = 0
OUTPUT = 1
LOW = 0
HIGH = 1

LED_PIN = 22

SONIC_TRIG = 23
SONIC_ECHO = 24

MOTION = 17

BUZZER = 25


LCD_GRND = 16
LCD_RS = 10
LCD_E = 9
LCD_D4 = 8
LCD_D5 = 7
LCD_D6 = 14
LCD_D7 = 15

SHUTDOWN_DELAY = 60

inactivity_timer = None
motion_sensor = None
distance_sensor = None
lcd = None
buzzer = None
led = None



def delay(delay_microseconds):
    time.sleep(delay_microseconds/1000000.0)


def delayMilli(delay_milliseconds):
    delay(delay_milliseconds * 1000)


def shutdown():
    global lcd
    global led

    if DEBUG:
        print("shutting down")
    led.off()
    lcd.off()


def wakeup():
    global lcd
    global led
    if DEBUG:
        print("waking up")
    led.on()
    lcd.on()



def main():
    global lcd
    global inactivity_timer
    global motion_sensor
    global lcd
    global buzzer
    global led


    wiringpi.wiringPiSetupGpio()


    print("Hallo")

    inactivity_timer = InactivityTimer(wakeup, shutdown, SHUTDOWN_DELAY)
    motion_sensor = MotionSensor(wiringpi, MOTION, inactivity_timer.trigger)
    distance_sensor = DistanceSensor(wiringpi, SONIC_ECHO, SONIC_TRIG)
    lcd = Display(LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7, LCD_GRND)
    buzzer = Buzzer(wiringpi, BUZZER)
    led = Led(wiringpi, LED_PIN)


    led.off()


    while True:
        if inactivity_timer.is_active():
            distance = distance_sensor.measure()

            distance_str = "{:13.2f}".format(distance)

            if DEBUG:
                print(distance_str + " cm")

            if wiringpi.millis() % 5 == 0:
                lcd.message(0, 0, distance_str + " cm")

            if distance > 0 and distance < 10:
                buzzer.beep(distance * 1000)

        delayMilli(100)

        inactivity_timer.loop()
        motion_sensor.sense()

        if DEBUG and inactivity_timer.is_active() == 1:
            print("shutting down in " + inactivity_timer.get_seconds_till_shutdown() + " seconds")
            lcd.message(0, 1, "SHUTDOWN in: " + inactivity_timer.get_seconds_till_shutdown().ljust(3))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        shutdown()
