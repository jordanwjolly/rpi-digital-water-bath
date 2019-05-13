#!/usr/bin/python

# This file contains all equations that a user can change
# A user enters the tank ID number into TANK_ENABLE to enable tanks
# A user needs to input the Sensor IDs themselves
import math


# Change the variables listed below as required by the experiment
class initialisation_variables:
    TANK_ENABLE = [1, 2, 3, 4]  # Specifies selected tanks
    ERROR_TOLERANCE = 0.1  # Allowable temperature error tolerance
    RUNTIME = 60 * 60 * 1  # Run time of experiment (seconds)
    GRAPH_SHOW = False  # NOT IMPLEMENTED
    REFRESH_TIME = 0.2  # Refresh rate of system (Seconds)) IS PER TANK
    COOLER_RECOVERY_TIME = 60  # seconds
    HEATER_RECOVERY_TIME = 10000  # seconds
    SENSOR_AVRG = 3  # num of readings per sensor for avr
    DUMMY = False  # can run on no RPi machine if True


# The Equations for our eight water tanks.
# To change the equation for a specifc relay, change the return value
# A more natural language reading of the function is " for a given relayID,
# return the set temperature for a given 't' "
# 't' is in seconds
def equations(relayID, t):
    t = float(t)  # casting to float (saftey)

    if relayID == 1:
        return 40 + 0.001 * 2 * t          # equation 1

    elif relayID == 2:
        return 22 + (5 * math.sin(0.0008 * t))  # equation 2

    elif relayID == 3:
        return 22 + 0.001 * 2 * 2 * t   # equation 3

    elif relayID == 4:
        return 22 + (2 * math.sin(0.0008 * t))  # equation 4

    elif relayID == 5:
        return 28 + (t / 2)  # equation 5

    elif relayID == 6:
        return 28 + (t / 2)  # equation 6

    elif relayID == 7:
        return 28 + (t / 2)  # equation 7

    elif relayID == 8:
        return 28 + (t / 2)  # equation 8
    else:
        return False


# This function returns the hardcoded addresses of the temperature sensors
# NOTE: keeping with convention, index starts at '1'.
# Sensor 1 for tank 1, is in the first place etc...
class sensor_ID:

    s1 = "28-000006dc6863"
    s2 = "28-000006dc76f3"
    s3 = "28-01131b65af91"
    s4 = "28-02131694dcaa"
    s5 = "28-01131e6b29e7"
    s6 = "28-01131b9be090"
    s7 = "28-0213139f02aa"
    s8= "28-01131bb70b6b"
