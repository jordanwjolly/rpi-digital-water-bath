#!/usr/bin/python

import subprocess
import time
import RPi.GPIO as gpio  # GPIO library

BOARD_MODE = gpio.BOARD  # The GPIO board mode setting
PIN_HEAT = 38  # Pin for heat unit.
PIN_COOL = 40  # Pin for "cooler


def setupGPIO():
    global BOARD_MODE
    global PIN_HEAT
    global PIN_COOL

    print('\nSetting up GPIO... \n')
    gpio.setwarnings(False)

    # Setting board mode.
    gpio.setmode(BOARD_MODE)

    # Setting up output pins
    gpio.setup(PIN_HEAT, gpio.OUT)
    gpio.setup(PIN_COOL, gpio.OUT)

    gpio.output(PIN_HEAT, True)
    gpio.output(PIN_COOL, True)

    print("Initially turn all systems off....\n")
    # setCooling(False, True)
    #heatingOn = [False, False, False, False, False, False, False, False]
    #coolingOn = [False, False, False, False, False, False, False, False]

    print('\nGPIO setup complete\n****************************************');
