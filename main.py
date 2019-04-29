#!/usr/bin/python


# TO DO
# Put function in BangBang class to get current temp automatically
# Overhaul multi-sensor temperature driver. is super slow and silly
# Loose the pickle format

# LIBRARIES
import os
import time
import sys
import signal
from Software_control import Controller
from Software_control import Data_logging
# from Hardware_control import WTI_control
from Hardware_control import Relay_control
from Hardware_control import Temp_sensor
import config

# Static Variables
DIR = os.path.dirname(os.path.realpath(__file__))
CURRENT_TEMP_FILE = DIR + '/Hardware_control/SensorValues.txt'
GRAPH_DIR = DIR + '/Data_Logging/'
INITIALISE = config.initialisation_variables()

if not INITIALISE.DUMMY:
    from Hardware_control import RPi_control


# Class which holds all temps/states/times
class TankVariables:

    def __init__(self, relay_id):
        self.Relay_ID = relay_id

    ERROR_TOLERANCE = INITIALISE.ERROR_TOLERANCE
    COOLER_RECOVERY_TIME = INITIALISE.COOLER_RECOVERY_TIME
    HEATER_RECOVERY_TIME = INITIALISE.HEATER_RECOVERY_TIME
    Current_Temp = float(0)  # SHOULD BE A CALLBACK FUNCTION
    Set_Temp = float(0)     # Set by controller
    Heater_State = False    # Current state
    Heater_Enable = False   # Future state
    Cooler_State = False
    Cooler_Enable = False
    Last_Heater_Enable = 0
    Last_Cooler_Disable = 0


# Allowing for graceful exit
def sigterm_handler(signal, frame):
    print('Exiting because of SIGTERM')
    sys.exit(0)


def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


def write_stdout(char_to_print):
    sys.stdout.flush()
    sys.stdout.write('\b')
    sys.stdout.write(char_to_print)


def time_step(current_time):
    return time.time() - current_time


def printCurrentState(
        Relay_ID, Current_Temp, Set_Temp, Heater_State, Cooler_State):
    print (
        'TANK #' + str(Relay_ID) + ": Curr=" + "{:.4f}".format(Current_Temp) +
        " Set=" + "{:.4f}".format(Set_Temp) + " Heat=" + str(Heater_State) +
        " Cool=" + str(Cooler_State))


# Main
def main():

    # Registering Handler
    signal.signal(signal.SIGTERM, sigterm_handler)

    # initialising each Tank object based of user input
    tank_list = [None, None, None, None, None, None, None, None]

    print(
        "\nRUNNING PROGRAM WITH FOLLOWING TANKS: " +
        str(INITIALISE.TANK_ENABLE) + "\n")

    for indx, Tank_ID in enumerate(INITIALISE.TANK_ENABLE):
        tank_list[indx] = TankVariables(Tank_ID)

    # Sets up GPIO pins for pi. Forces all relays into off state.
    if not INITIALISE.DUMMY:
        RPi_control.setupGPIO()
        Relay_control.RelayInitialse(INITIALISE.TANK_ENABLE)

    # MAIN Super Loop
    TIME_STEP_THRESH = INITIALISE.REFRESH_TIME * len(INITIALISE.TANK_ENABLE)
    t = 0

    while (t < INITIALISE.RUNTIME):  # Uses secs, range time > with # of tanks

        current_time = time.time()  # for time step
        # Print nice output, ready for next graph
        print("\n#######################################################")
        print "Runtime: " + "{:.4f}".format(t) + " Secs"

        # Loops through list, updates controller, and actuates if needed
        for tank in tank_list:

            if tank is None:  # None exists for all non-tanks
                continue

            # Updates current temperature
            tank.Current_Temp = Temp_sensor.current_temp(tank.Relay_ID)
            tank.Set_Temp = config.equations(tank.Relay_ID, t)

            # Checks state, to see if state change required
            tank.Heater_Enable, tank.Cooler_Enable = Controller.controller(
                tank.Set_Temp, tank.Current_Temp, tank.Heater_State,
                tank.Cooler_State, tank.ERROR_TOLERANCE)

            # Checks Validity of state change (based off hardware constraints)
            if Controller.HeaterCheck(
                    tank.Heater_Enable, tank.Cooler_State,
                    tank.Last_Heater_Enable, tank.HEATER_RECOVERY_TIME):

                tank.Heater_Enable = not tank.Heater_Enable

            if Controller.CoolerCheck(
                    tank.Cooler_Enable, tank.Heater_State,
                    tank.Last_Cooler_Disable, tank.COOLER_RECOVERY_TIME):

                tank.Cooler_Enable = not tank.Cooler_Enable

            # Controls hardware relays connected to the WTI ethernet switch
            if not tank.Heater_State == tank.Heater_Enable:

                # Turn the relay on/off. Returns current state of relay
                Relay_check = Relay_control.relayLogic(
                    tank.Heater_Enable, tank.Relay_ID, INITIALISE.DUMMY)

                if not tank.Heater_State and tank.Heater_Enable:
                    tank.Last_Heater_Enable = time.time()

                # Changing last state heater
                tank.Heater_State = Relay_check
                # tank.Heater_State = tank.Heater_Enable

            # Changes state of Cooler and actuates (DISABLED)
            if not tank.Cooler_State == tank.Cooler_Enable:

                # # Turn the relay on/off. Returns current state of relay
                # Relay_check = Relay_control.relayLogic(
                #     tank.Heater_Enable, tank.Relay_ID, INITIALISE.DUMMY)

                # Updating last state of cooler
                tank.Cooler_State = tank.Cooler_Enable

                if not tank.Cooler_Enable:
                    tank.Last_Cooler_Disable = time.time()

            # Display current state
            printCurrentState(
                tank.Relay_ID, tank.Current_Temp, tank.Set_Temp,
                tank.Heater_State, tank.Cooler_State)

            # Saves current values for tank 'x' to csv
            Data_logging.saveCurrentState(
                t, tank.Set_Temp, tank.Current_Temp, tank.Relay_ID,
                tank.Heater_State, tank.Heater_Enable,
                tank.Last_Heater_Enable, tank.Cooler_State,
                tank.Cooler_Enable, tank.Last_Cooler_Disable,
                GRAPH_DIR)

            # update GUI graph results
            if INITIALISE.GRAPH_SHOW:
                Data_logging.updateGraph(GRAPH_DIR, tank.Relay_ID)
                print("WOW...Graph")

        spinner = spinning_cursor()

        TIME_STEP = time_step(current_time)

        while TIME_STEP < TIME_STEP_THRESH:
            time. sleep(0.1)
            write_stdout(next(spinner))
            TIME_STEP = time_step(current_time)
        write_stdout(" ")

        # Updates t based off most current time delta
        t = t + time_step(current_time)


####################################
if __name__ == "__main__":
    main()
