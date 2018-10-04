#!/usr/bin/python
#FUTURE WORK:   Have the WTI bash scripts run in the background (so it doesn't block main)
#               Overhaul multi-sensor temperature driver... is super slow and silly. Make them run in parallel
#               Fix the implementation of timestep in super loop. Is currently invalid
#               Graphing of output
#               Put function in BangBang class to get current temp automatically


# LIBRARIES
import os, time, math, csv
#import numpy as np
from Software_control import BangBang_Controller
from Software_control import Graph_show
from Hardware_control import WTI_control
import config

# Static Variables
DIR = os.path.dirname(os.path.realpath(__file__))
CURRENT_TEMP_FILE = DIR + '/Hardware_control/SensorValues.txt'
GRAPH_FILE = DIR + '/Software_control/Graph_values.csv'
INITIALISE = config.initialisationVariables()    # Hack to bring vars in from config. breaks loop if config incorrect

# Class which holds all temps/states/times
class TankVariables:

    def __init__(self, relay_id, sensor_address):
        self.Relay_ID = relay_id
        self.Sensor_Address = sensor_address

    ERROR_TOLERANCE = INITIALISE.ERROR_TOLERANCE
    COOLER_TIME = INITIALISE.HEATER_RECOVERY_TIME
    HEATER_TIME = INITIALISE.COOLER_RECOVERY_TIME
    Current_Temp = float(0) # Should have function to retreive most current temp automatically
    Set_Temp = float(0)     # Set by controller
    Heater_State = False    # Current state
    Heater_Enable = False   # Future state
    Cooler_State = False
    Cooler_Enable = False
    Last_Heater_Disable = time.time()
    Last_Cooler_Disable = time.time()


# Main
BangBang_Controller.setupGPIO() #Sets up GPIO pins for pi

#initialising each Tank object based of user input
tank_list=[]
for indx, Tank_ID in enumerate(INITIALISE.TANK_ENABLE):
    tank_list[indx] = TankVariables(Tank_ID, config.sensor_ID(Tank_ID))

# Super Loop
for t in range(0, INITIALISE.RUNTIME * 60 * 60):

    # Get current Temperature
    currTemps = BangBang_Controller.currTemp(CURRENT_TEMP_FILE)

    # Loops through list of controller objects, updates controller, and actuates if needed
    for tank in tank_list:

        # Updates current temperature
        tank.Current_Temp=currTemps[0] #FIX FIX FIX FIX FIX

        # Checks state, to see if state change required
        print('\nTesting Tank: ' + tank.Relay_ID)
        tank.Heater_Enable, tank.Cooler_Enable = BangBang_Controller.controller(tank.Set_Temp,
                                    tank.Current_Temp, tank.Heater_State, tank.Cooler_State, tank.ERROR_TOLERANCE)

        # Checks Validity of state change (Based hardware constraints)
        tank.Heater_State = BangBang_Controller.HeatCheck(tank.Heater_State, tank.Cooler_State,
                                                          tank.Last_Heater_Disable, tank.HEATER_TIME)
        tank.Cooler_State = BangBang_Controller.CoolerCheck(tank.Heater_State, tank.Cooler_State,
                                                            tank.Last_Cooler_Disable, tank.COOLER_TIME)

        # Changes state #Currently only does heater
        if not tank.Heater_State == tank.Heater_Enable:
            tank.Last_Heater_Disable = WTI_control.WTI_logic(tank.Heater_Enable, DIR, tank.Relay_ID)
        #if not tank.Cooler_State == tank.Cooler_Enable:
         #   tank.Last_Cooler_Disable = WTI_control.WTI_logic(tank.Cooler_Enable, DIR, tank.Relay_ID)

    print("#######################################################\n")

    # Update graph
    if INITIALISE.GRAPH_SHOW:
         Graph_show.updateGraph(SetTemps, currTemps, GRAPH_FILE)
        #Graph_show.SaveCurrentValues(SetTemps, currTemps, GRAPH_FILE)

    # Sets delay between reading intervals (should be larger than 5 seconds)
    time.sleep(INITIALISE.TIME_STEP) #

