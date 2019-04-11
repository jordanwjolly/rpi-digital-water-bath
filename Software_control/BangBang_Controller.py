#!/usr/bin/python

# Imports ##############################################################################################################
########################################################################################################################

import os  # OS functions
import time  # Time functions

# Functions ############################################################################################################
########################################################################################################################

# TURNS ON THE COOLER
def CoolerCheck(Cooler_Enable, Heater_State, Last_Cooler_Disable, COOLER_RECOVERY_TIME):

    # If we want to change state, double check is valid
    if Cooler_Enable:

        # Cannot enable heating if A/C is on
        if Heater_State:
            print('*** Cannot enable cooling if heating is on. Disabling heating first! ***')
            return not Cooler_Enable
            return not Heater_Enable #need both heating and cooling to be off

        #cannot enable if is in recovery period
        elif int(time.time()) < (Last_Cooler_Disable + COOLER_RECOVERY_TIME):
            print('*** Cannot enable cooling, cooling in recovery ***')
            return not Cooler_Enable

        print('*** Cooling stays on ***')
        return Cooler_Enable

    # Heating stays off
    elif not Cooler_Enable:
        print('*** Cooling stays off ***')
        return Cooler_Enable

    #Error handling
    else:
        print("Cooler_Enable variable is incorrect")


# Checks heater state against cooler state, and cooldown period
def HeatCheck(Heater_Enable, Cooler_State, Last_Heater_Enable, HEATER_RECOVERY_TIME):

    # If we want to change state, double check is valid
    if Heater_Enable:

        # Cannot enable heating if A/C is on
        if Cooler_State:
            print('*** Cannot enable heating if cooling is on. Disabling cooling first! ***')
            return not Heater_Enable
            return not Cooler_Enable #need both heating and cooling to be off

        #cannot enable if is in recovery period
        elif int(time.time()) < (Last_Heater_Enable + HEATER_RECOVERY_TIME):

            print('*** Cannot enable heating, heater in recovery ***')
            return not Heater_Enable

        print('*** Heating stays on ***')
        return Heater_Enable

    # Heating stays off
    elif not Heater_Enable:
        print('*** Heating stays off ***')
        return Heater_Enable
    
    # Error handling
    else:
        print ("Heater_Enable variable is incorrect")


def controller(setTemp, currTemp, Cooler_Enable, Heater_Enable, threshold):

    hotterThanSet = False
    coolerThanSet = False

    heating_state = False #return values
    cooling_state = False

    # CHECKING TO SEE IF TEMP IS ABOVE/BELOW SET POINT
    # COOLER: Cooler is on, it should stay on until it goes past the threshold
    if (Cooler_Enable and (setTemp < (currTemp + threshold))):
        hotterThanSet = True
    # COOLER: Cooler is currently off, it should turn on when it hits the threshold
    if ((not Cooler_Enable) and (setTemp < (currTemp - threshold))):
        hotterThanSet = True
    # HEATER: Heater is on, it should stay on until it goes past the threshold
    if (Heater_Enable and (setTemp > (currTemp - threshold))):
        coolerThanSet = True
    # HEATER: Heater is currently off, it should turn on when it hits the threshold
    if ((not Heater_Enable) and (setTemp > (currTemp + threshold))):
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
