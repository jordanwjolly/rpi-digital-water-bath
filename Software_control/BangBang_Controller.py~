#!/usr/bin/python

# Imports ##############################################################################################################
########################################################################################################################

import os  # OS functions
import time  # Time functions

# Functions ############################################################################################################
########################################################################################################################

# TURNS ON THE COOLER
def CoolerCheck(coolingOn, heatingState, lastCoolerDisableTime, COOLER_RECOVERY_TIME):

    # If we want to change state, double check is valid
    if coolingOn:

        # Cannot enable heating if A/C is on
        if heatingState:
            print('*** Cannot enable cooling if heating is on. Disabling heating first! ***')
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
            print('*** Cannot enable heating if cooling is on. Disabling cooling first! ***')
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
