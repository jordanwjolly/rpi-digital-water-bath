#!/usr/bin/python

# LIBRARIES
import os, time, math, csv
import numpy as np
from Software_control import Actuator_control
from Software_control import Graph_show

# FILE PATH INFO
DIR = dir_path = os.path.dirname(os.path.realpath(__file__))
CURRENT_TEMP_FILE = DIR+'/Hardware_control/SensorValues.txt'
SENSOR_SCRIPT_FILE = DIR + '/Hardware_control/Temp_sensor.py'
GRAPH_FILE = DIR + '/Software_control/Graph_values.csv'

# Sets up everything
Actuator_control.setupGPIO()
SetTemps = np.array([0,0,0,0,0,0,0,0], dtype=np.float) #Initiates an 1x8 array of NaNs
SetTemps.fill(np.nan)
CurrTemps=SetTemps



############MAIN CODE#####################
##########################################

# Choose the variables
ERROR_TOLERANCE = 0.05		#Allowable temperature error tolerance
RUNTIME = 1 									#Run time of experiment (Is specified in hours)
GRAPH_SHOW= True				#Toggle True/False to show graphical output of temp profile
TIME_STEP = 5 								# Refresh rate of sensors (Seconds))

# Range of time
for t in range(0, RUNTIME*60*60):

	# The Equations for our eight water tanks.
 	# Uncomment for every tank in use
	SetTemps[0] = 28# +(float(t)/2) 		#equation 1
	SetTemps[1] = 25.6+(float(t)/200) 	#eqn 2
	#SetTemps[2] = 28+(float(t)/2) 		#3
	#SetTemps[3] = 28+(float(t)/2) 		#4
	#SetTemps[4] = 28+(float(t)/2) #temperature
	#SetTemps[5] = 28+(float(t)/2) #temperature
	#SetTemps[6] = 28+(float(t)/2) #temperature
	#SetTemps[7] = 28+(float(t)/2) #temperature

	# Get current Temperature
	currTemps = Actuator_control.currTemp(CURRENT_TEMP_FILE)

	# Does all of the stuff
	for relayID, val in enumerate(SetTemps):
		if np.isnan(val):
			continue
		else:		
			Actuator_control.checkClimate(SetTemps[relayID], float(currTemps[relayID]), ERROR_TOLERANCE, DIR, relayID) 
	print("#######################################################\n")
	
	# Update graph
	if (GRAPH_SHOW): 	
		#Graph_show.updateGraph(SetTemps, currTemps, GRAPH_FILE)
		Graph_show.SaveCurrentValues(SetTemps, currTemps, GRAPH_FILE)
	
	# Sets delay between reading intervals (should be larger than 5 seconds)
	time.sleep(TIME_STEP)

# Turns off everything at end of experiment
Actuator_control.goodbye()
