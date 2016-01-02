#!/usr/bin/env/python

import time

import wiringpi2 as wiringpi
from helper.InactivityTimer import InactivityTimer
from sensors.MotionSensor import MotionSensor
from sensors.DistanceSensor import DistanceSensor
from sensors.Display import Display
from sensors.Buzzer import Buzzer
from sensors.Led import Led
import configuration as config


# Globals
INPUT = 0
OUTPUT = 1
LOW = 0
HIGH = 1

inactivity_timer = None
motion_sensor = None
distance_sensor = None
lcd = None
buzzer = None
led = None
last_pullup_time = 0

pullup_count_today = 0
pullup_count_alltime = 0
pullups_to_go = config.PULLUPS_PER_DAY


def delay(delay_microseconds):
    time.sleep(delay_microseconds/1000000.0)


def delay_milli(delay_milliseconds):
    delay(delay_milliseconds * 1000)


def shutdown():
    global lcd
    global led

    if config.DEBUG:
        print("shutting down")
    led.off()
    lcd.off()


def wakeup():
    global lcd
    global led
    global pullup_count_alltime
    if config.DEBUG:
        print("waking up")
    led.on()
    lcd.on()
    lcd.message(0, 0, "Welcome ATHLETE!")
    lcd.message(0, 1, str(pullup_count_alltime) + " Pullups")


def count_pullup():
    global pullup_count_today
    global pullups_to_go
    global pullup_count_alltime
    global last_pullup_time

    pullup_count_today += 1
    pullup_count_alltime += 1
    pullups_to_go -= 1

    last_pullup_time = wiringpi.millis()
    return pullup_count_today


def main():
    global lcd
    global inactivity_timer
    global motion_sensor
    global distance_sensor
    global lcd
    global buzzer
    global led
    global last_pullup_time
    global pullup_count_alltime
    global pullups_to_go

    wiringpi.wiringPiSetupGpio()

    inactivity_timer = InactivityTimer(wakeup, shutdown, config.SHUTDOWN_DELAY)
    motion_sensor = MotionSensor(wiringpi, config.MOTION, inactivity_timer.trigger)
    distance_sensor = DistanceSensor(wiringpi, config.SONIC_ECHO, config.SONIC_TRIG)
    lcd = Display(config.LCD_RS, config.LCD_E, config.LCD_D4, config.LCD_D5, config.LCD_D6, config.LCD_D7, config.LCD_K)
    buzzer = Buzzer(wiringpi, config.BUZZER)
    led = Led(wiringpi, config.LED_PIN)

    distance_resetted = True

    shutdown()

    while True:
        if inactivity_timer.is_active():
            distance = distance_sensor.measure()

            distance_str = "{:13.2f}".format(distance)

            if config.DEBUG:
                print(distance_str + " cm")
                # if wiringpi.millis() % 5 == 0:
                #     lcd.message(0, 0, distance_str + " cm")

            # only count a pullup if:
            # - distance is smaller than 5cm
            # - distance was resetted (athlete moved more than 20 cm away from sensor)
            # - last pullup was done more than 1 second ago
            if 0 < distance < config.COUNT_DISTANCE and distance_resetted and wiringpi.millis() > (last_pullup_time + config.RESET_TIME):
                buzzer.beep(5000)
                distance_resetted = False
                cnt = count_pullup()
                lcd.clear()
                lcd.message(0, 0, "Pullups: " + str(cnt).rjust(5))
                lcd.message(0, 1, "2do2day: " + str(pullups_to_go).rjust(5))
            elif distance > config.RESET_DISTANCE:
                distance_resetted = True

        delay_milli(100)

        inactivity_timer.loop()
        motion_sensor.sense()

        if config.DEBUG and inactivity_timer.is_active() == 1:
            print("shutting down in " + inactivity_timer.get_seconds_till_shutdown() + " seconds")
            # lcd.message(0, 1, "SHUTDOWN in: " + inactivity_timer.get_seconds_till_shutdown().ljust(3))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        shutdown()
