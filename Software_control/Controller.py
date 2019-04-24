#!/usr/bin/python

# Imports ##############################################################################################################
########################################################################################################################

import os  # OS functions
import time  # Time functions

# Functions ############################################################################################################
########################################################################################################################

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
        return heating_state, cooling_state

    if ((not hotterThanSet) and (not coolerThanSet)):

        heating_state = False
        cooling_state = False
        return heating_state, cooling_state

    elif (hotterThanSet):
        heating_state = False
        cooling_state = True
        return heating_state, cooling_state


    elif (coolerThanSet):
        heating_state = True
        cooling_state = False
        return heating_state, cooling_state

# Checks heater state against cooler state, and cooldown period
def HeaterCheck(Heater_Enable, Cooler_State, Last_Heater_Enable, HEATER_RECOVERY_TIME):

    Heater_Check=False

    # If we want to change state, double check is valid
    if Heater_Enable:

        # Cannot enable heating if cooling is on
        if Cooler_State:
            print('*** Cannot enable heating if cooling is on! ***')
            return not Heater_Check

        #cannot enable if is in recovery period
        elif ((time.time() - Last_Heater_Enable) > HEATER_RECOVERY_TIME) and Last_Heater_Enable: #checking last heater enable for edge case of initialisation to '0'

            if ((time.time() - Last_Heater_Enable) > HEATER_RECOVERY_TIME*2):
                print('________Enabling Heating, Heater timeout period over! ***')
                return Heater_Check
            else:
                print('________Cannot enable heating, heater in timeout ***')
                return not Heater_Check

        return Heater_Check

    # Heating stays off
    elif not Heater_Enable:
        
        return Heater_Check
    
    # Error handling
    else:
        print ("Heater_Enable variable is incorrect")

# TURNS ON THE COOLER
def CoolerCheck(Cooler_Enable, Heater_State, Last_Cooler_Disable, COOLER_RECOVERY_TIME):

    Cooler_Check=False

    # If we want to change state, double check is valid
    if Cooler_Enable:

        # Cannot enable heating if cooling is on
        if Heater_State:
            print('*** Cannot enable cooling if heating is on! ***')
            return not Cooler_Check

        #cannot enable if is in recovery period
        elif int(time.time()) < (Last_Cooler_Disable + COOLER_RECOVERY_TIME):
            print('*** Cannot enable cooling, cooling in recovery ***')
            return not Cooler_Check

        return Cooler_Check

    # Heating stays off
    elif not Cooler_Enable:

        return Cooler_Check

    #Error handling
    else:
        print("Cooler_Enable variable is incorrect")

