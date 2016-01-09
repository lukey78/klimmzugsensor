__author__ = 'Jens'

# DATABASE config

DB_HOST = "localhost"
DB_NAME = "pullups"
DB_USER = "pullup"
DB_PASS = "pulluppass456"


# SYSTEM config

# turn on or off debugging mode (logging in console)
DEBUG = 0

# after how many seconds the sensor should go to standby mode (turning off display)
SHUTDOWN_DELAY = 60

# the max distance from the sensor to the head of the athlete where a pullup should be counted (cm)
COUNT_DISTANCE = 5
# the min distance the athlete's head has to move away from the sensor to reset the cheat counter (cm)
RESET_DISTANCE = 20

# the milliseconds an athlete's head has to stay away from the sensor (more then RESET_DISTANCE away)
# to reset the cheat counter
RESET_TIME = 1000

# PULLUPs config
PULLUPS_PER_DAY = 50


# PIN config (GPIO pin numbering)
LED_PIN = 18

SONIC_TRIG = 23
SONIC_ECHO = 24

MOTION = 14

BUZZER = 15

LCD_RS = 25
LCD_E = 8
LCD_D4 = 7
LCD_D5 = 1
LCD_D6 = 12
LCD_D7 = 16
LCD_K = 20


