#!/usr/bin/python
#FUTURE WORK:   Have the WTI bash scripts run in the background (so it doesn't block main)
#               Overhaul multi-sensor temperature driver... is super slow and silly. Make them run in parallel
#               Fix the implementation of timestep in super loop. Is currently invalid
#               Graphing of output
#               Put function in BangBang class to get current temp automatically


# LIBRARIES
import os, time, math, csv, sys, signal
#import numpy as np
from multiprocessing import Process
from Software_control import BangBang_Controller
#from Software_control import Graph_show
from Hardware_control import WTI_control
from Hardware_control import Temp_sensor
import config

# Static Variables
DIR = os.path.dirname(os.path.realpath(__file__))
CURRENT_TEMP_FILE = DIR + '/Hardware_control/SensorValues.txt'
GRAPH_FILE = DIR + '/Software_control/Graph_values.csv'
INITIALISE = config.initialisationVariables()    # Hack to bring vars in from config. breaks loop if config incorrect

# Class which holds all temps/states/times
class TankVariables:

    def __init__(self, relay_id):
        self.Relay_ID = relay_id

    ERROR_TOLERANCE = INITIALISE.ERROR_TOLERANCE
    COOLER_TIME = INITIALISE.COOLER_RECOVERY_TIME
    HEATER_TIME = INITIALISE.HEATER_RECOVERY_TIME
    Current_Temp = float(0) # Should have function to retreive most current temp automatically
    Set_Temp = float(0)     # Set by controller
    Heater_State = False    # Current state
    Heater_Enable = False   # Future state
    Cooler_State = False
    Cooler_Enable = False
    Last_Heater_Disable = 0
    Last_Cooler_Disable = 0

#Allowing for graceful exit
def sigterm_handler(signal, frame):
    # save the state here or do whatever you want
    print('Exiting because of SIGTERM')
    sys.exit(0)

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

# Main
def main():
   
    #Registering Handler
    signal.signal(signal.SIGTERM, sigterm_handler)

    #Flag which allows dummy data for testing
    if len(sys.argv) > 1:
        if sys.arv[1]=="Dummy":
            print("** Dummy data is being used for testing!! **")
            Dummy_Flag=True

    #initialising each Tank object based of user input
    tank_list=[None, None, None, None, None, None, None, None]
    print("\nRUNNING PROGRAM WITH FOLLOWING TANKS: "+str(INITIALISE.TANK_ENABLE)+"\n")
    for indx, Tank_ID in enumerate(INITIALISE.TANK_ENABLE):
        tank_list[indx] = TankVariables(Tank_ID)
    
    #Sets up GPIO pins for pi
    BangBang_Controller.setupGPIO()
    #Process(target=Temp_Sensor.start_temp_sensor(config.sensor_ID), args=(config.sensor_ID)).run() #starts temp sensor process

    # MAIN Super Loop
    for t in range(0, INITIALISE.RUNTIME * 60 * 60, INITIALISE.TIME_STEP):
        
        current_time = time.time()

        # Get current Temperature
        currTemps = 22.3#BangBang_Controller.currTemp(CURRENT_TEMP_FILE)

        # Loops through list of controller objects, updates controller, and actuates if needed
        for tank in tank_list:
           
            if tank == None: # None exists for all non-tanks
                continue

            # Updates current temperature
            tank.Current_Temp= currTemps #FIX FIX FIX FIX FIX
            tank.Set_Temp = config.equations(tank.Relay_ID, t)

            # Checks state, to see if state change required
            print('\nTesting Tank: ' + str(tank.Relay_ID))
            tank.Heater_Enable, tank.Cooler_Enable = BangBang_Controller.controller(tank.Set_Temp,
                                        tank.Current_Temp, tank.Heater_State, tank.Cooler_State, tank.ERROR_TOLERANCE)

            # Checks Validity of state change (Based hardware constraints)
            tank.Heater_Enable = BangBang_Controller.HeatCheck(tank.Heater_Enable, tank.Cooler_State,
                                                              tank.Last_Heater_Disable, tank.HEATER_TIME)
            tank.Cooler_Enable = BangBang_Controller.CoolerCheck(tank.Cooler_Enable, tank.Heater_State,
                                                                tank.Last_Cooler_Disable, tank.COOLER_TIME)

            # Changes state of Heater and actuates (If required)
            if not tank.Heater_State == tank.Heater_Enable:
                
                WTI_control.WTI_logic(tank.Heater_Enable, DIR, tank.Relay_ID) #Turn the relay on/off
                tank.Heater_State = tank.Heater_Enable #changing last state heater

                if not tank.Heater_Enable: # updating last disable time
                    tank.Last_Heater_Disable = time.time()
                
            # Changes state of Cooler and actuates (If required)
            if not tank.Cooler_State == tank.Cooler_Enable:
                
                print("IF WE HAD A COOLER, I WOULD CHANGE THE STATE NOW")
                # WTI_control.WTI.logic(tank.Cooler_Enable, DIR, tank.Relay_ID) #This will change a relay
                tank.Cooler_State = tank.Cooler_Enable #Updating last state of cooler
                
                if not tank.Cooler_Enable: # updating last disable time
                    tank.Last_Cooler_Disable = time.time()

            #Saves current values for tank 'x' to csv
            if INITIALISE.GRAPH_SHOW:
                #Graph_show.saveCurrentValue(time.time(), tank.Set_Temp, tank.Current_Temp, tank.Relay_ID)
                print("Updated values of graph")
        # update GUI graph results
        if INITIALISE.GRAPH_SHOW:
            # Graph_show.updateGraph(INITIALISE.TANK_ENABLE)
            print("WOW...Graph")

         # Print nice output, ready for next graph
        print("#######################################################\n")
         
        spinner=spinning_cursor() 
        # ensures that the loop is remaining within the given TIME_STEP
        while ((time.time()-current_time) < INITIALISE.TIME_STEP): #
            time. sleep(0.1)
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            sys.stdout.write('\b')
                    

###################################
if __name__ == "__main__":
    main()
