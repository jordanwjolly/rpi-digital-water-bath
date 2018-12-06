#!/usr/bin/python
#FUTURE WORK:   DONE: Have the WTI bash scripts run in the background (so it doesn't block main)
#               DONE: Fix the implementation of timestep in super loop. Is currently invalid
#               DONE: Put fancy spinning cursor while waiting for next time-step

#TO DO!!!!
#Fix up the temp logger file, has relance on old global vars
#               sub-plotting of output graphs
#               Put function in BangBang class to get current temp automatically
#               Overhaul multi-sensor temperature driver... is super slow and silly. Make them run in parallel

# LIBRARIES
import os, time, csv, sys, signal
#import numpy as np
from multiprocessing import Process
from Software_control import BangBang_Controller
from Software_control import Temp_Grapher
from Hardware_control import WTI_control
from Hardware_control import Temp_sensor
import config

# Static Variables
DIR = os.path.dirname(os.path.realpath(__file__))
CURRENT_TEMP_FILE = DIR + '/Hardware_control/SensorValues.txt'
GRAPH_DIR = DIR + '/Graph_data/'
INITIALISE = config.initialisationVariables()    # Hack to bring vars in from config. breaks loop if config incorrect

if not INITIALISE.DUMMY:
    from Hardware_control import RPi_control

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

    #initialising each Tank object based of user input
    tank_list=[None, None, None, None, None, None, None, None]
    print("\nRUNNING PROGRAM WITH FOLLOWING TANKS: "+str(INITIALISE.TANK_ENABLE)+"\n")
    for indx, Tank_ID in enumerate(INITIALISE.TANK_ENABLE):
        tank_list[indx] = TankVariables(Tank_ID)
    
    #Sets up GPIO pins for pi. SHOULD START TEMP SENSOR HERE
    if not INITIALISE.DUMMY:
        RPi_control.setupGPIO()
        #Process(target=Temp_Sensor.start_temp_sensor(config.sensor_ID), args=(config.sensor_ID)).run() #starts temp sensor process

    # MAIN Super Loop
    TIME_STEP = INITIALISE.REFRESH_TIME * len(INITIALISE.TANK_ENABLE)
    for t in range(0, INITIALISE.RUNTIME, TIME_STEP): #Is calculated in seconds, range time skip increases based of # of tanks

        current_time = time.time() #getting current time for TIME_STEP validation
        print (current_time)
        print(type(current_time))

        # Loops through list of controller objects, updates controller, and actuates if needed
        for tank in tank_list:
           
            if tank == None: # None exists for all non-tanks
                continue

            # Updates current temperature
            tank.Current_Temp = Temp_sensor.current_temp(tank.Relay_ID)
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
                
                WTI_control.WTI_logic(tank.Heater_Enable, DIR, tank.Relay_ID, INITIALISE.DUMMY) #Turn the relay on/off
                tank.Heater_State = tank.Heater_Enable #changing last state heater

                if not tank.Heater_Enable: # updating last disable time
                    tank.Last_Heater_Disable = time.time()
                
            # Changes state of Cooler and actuates (If required)
            if not tank.Cooler_State == tank.Cooler_Enable:
                
                print("IF WE HAD A COOLER, I WOULD CHANGE THE STATE NOW")
                # WTI_control.WTI.logic(tank.Cooler_Enable, DIR, tank.Relay_ID,  DUMMY) #This will change a relay
                tank.Cooler_State = tank.Cooler_Enable #Updating last state of cooler
                
                if not tank.Cooler_Enable: # updating last disable time
                    tank.Last_Cooler_Disable = time.time()

            #Saves current values for tank 'x' to csv
            Temp_Grapher.saveCurrentValue(tank.Set_Temp, tank.Current_Temp, tank.Relay_ID, GRAPH_DIR)
            #print("Updated values of graph")

            # update GUI graph results
            if INITIALISE.GRAPH_SHOW:
                Temp_Grapher.updateGraph(GRAPH_DIR, tank.Relay_ID)
                print("WOW...Graph")

         # Print nice output, ready for next graph
        print("#######################################################\n")
         
        spinner=spinning_cursor() 
        # ensures that the loop is remaining within the given TIME_STEP
        #pPUT LOGIC HERE TO STATE IF LOOP USES MORE TIME THAN TIMESTEP
        while ((time.time()-current_time) < TIME_STEP): #
            time. sleep(0.1)
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            sys.stdout.write('\b')

###################################
if __name__ == "__main__":
    main()
