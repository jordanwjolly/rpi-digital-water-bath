#!/usr/bin/python

# Imports ##############################################################################################################
########################################################################################################################

import os  # OS functions
import RPi.GPIO as gpio  # GPIO library
import time  # Time functions
import pickle

# Constants ############################################################################################################
########################################################################################################################
# Save path of current temperature
DIR = dir_path = os.path.dirname(os.path.realpath(__file__))
CURRENT_FILE = DIR + '/SensorValues.txt'


# Relay pins
BOARD_MODE = gpio.BOARD  # The GPIO board mode setting
PIN_HEAT = 38  # Pin for heat unit.
PIN_COOL = 40  # Pin for "cooler
TOGGLE_DELAY = 1

# Functions ############################################################################################################
########################################################################################################################


def delay():
    global TOGGLE_DELAY
    time.sleep(TOGGLE_DELAY)


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
    heatingOn = [False, False, False, False, False, False, False, False]
    coolingOn = [False, False, False, False, False, False, False, False]

    print('\nGPIO setup complete\n****************************************');


def currTemp(CURRENT_TEMP_FILE):
    currTemp = pickle.load(open(CURRENT_TEMP_FILE, 'r'))
    return currTemp

# TURNS ON THE COOLER
def CoolerCheck(coolingOn, heatingState, lastCoolerDisableTime, COOLER_RECOVERY_TIME):

    # If we want to change state, double check is valid
    if coolingOn:

        # Cannot enable heating if A/C is on
        if heatingState:
            print('*** Cannot enable cooling if heating is on. Must disable heating first! ***')
            return not coolingOn

        #cannot enable if is in recovery period
        elif int(time.time()) < (lastCoolerDisableTime + COOLER_RECOVERY_TIME):
            print('*** Cannot enable cooling, cooling in recovery ***')
            return not coolingOn

        print('*** Cooling stays on ***')
        return coolingOn

    # Heating stays off
    elif not coolingOn:
        print('*** Cooling stays off ***')
        return coolingOn

    #Error handling
    else:
        print("coolingOn variable is incorrect")


# Checks heater state against cooler state, and cooldown period
def HeatCheck(heatingOn, coolingState, lastHeaterDisableTime, HEATER_RECOVERY_TIME):

    # If we want to change state, double check is valid
    if heatingOn:

        # Cannot enable heating if A/C is on
        if coolingState:
            print('*** Cannot enable heating if cooling is on. Must disable cooling first! ***')
            return not heatingOn

        #cannot enable if is in recovery period
        elif int(time.time()) < (lastHeaterDisableTime + HEATER_RECOVERY_TIME):

            print('*** Cannot enable heating, heater in recovery ***')
            return not heatingOn

        print('*** Heating stays on ***')
        return heatingOn

    # Heating stays off
    elif not heatingOn:
        print('*** Heating stays off ***')
        return heatingOn
    
    # Error handling
    else:
        print ("heatingOn variable is incorrect")


def controller(setTemp, currTemp, coolingOn, heatingOn, threshold):

    hotterThanSet = False
    coolerThanSet = False

    heating_state = False #return values
    cooling_state = False

    # CHECKING TO SEE IF TEMP IS ABOVE/BELOW SET POINT
    # COOLER: Cooler is on, it should stay on until it goes past the threshold
    if (coolingOn and (setTemp < (currTemp + threshold))):
        hotterThanSet = True
    # COOLER: Cooler is currently off, it should turn on when it hits the threshold
    if ((not coolingOn) and (setTemp < (currTemp - threshold))):
        hotterThanSet = True
    # HEATER: Heater is on, it should stay on until it goes past the threshold
    if (heatingOn and (setTemp > (currTemp - threshold))):
        coolerThanSet = True
    # HEATER: Heater is currently off, it should turn on when it hits the threshold
    if ((not heatingOn) and (setTemp > (currTemp + threshold))):
        coolerThanSet = True

    # TURN THE HEATER/COOLER ON/OFF
    if (hotterThanSet and coolerThanSet):
        print("Current: " + str(currTemp) + " Set-point: " + str(setTemp))
        print('*** Error: Outside of both ranges somehow.')
        return heating_state, cooling_state

    if ((not hotterThanSet) and (not coolerThanSet)):
        print('Temperature is in range, no actuation required')
        print("Current: " + str(currTemp) + " Set-point: " + str(setTemp) + " Heating: OFF Cooler: OFF")

        heating_state = False
        cooling_state = False
        return heating_state, cooling_state

    elif (hotterThanSet):
        print('Water temperature is too warm')
        print("Current: " + str(currTemp) + " Set-point: " + str(setTemp) + " Heating: OFF Cooler: ON")

        heating_state = False
        cooling_state = True
        return heating_state, cooling_state


    elif (coolerThanSet):
        print('Water temperature is too cold')
        print("Current: " + str(currTemp) + " Set-point: " + str(setTemp) + " Heating: ON Cooler: OFF")

        heating_state = True
        cooling_state = False
        return heating_state, cooling_state
