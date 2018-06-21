#!/usr/bin/python

# This file dictates what the heating profile looks like
import os
import time			# Time functions
from Software_control import Actuator_control
from Software_control import Graph_show

ERROR_TOLERANCE = 0.1
#Save path of current temperature
DIR = dir_path = os.path.dirname(os.path.realpath(__file__))
CURRENT_FILE = DIR+'/current.json'


# Sets up everything
Actuator_control.setupGPIO()

# Range of time
for t in range(0, 1000):

	# The Equation
	setTemp = 20+float(t)/2

	# Get current Temperature
	currTemp = Actuator_control.currTemp(CURRENT_FILE)

	# Does all of the stuff
	Actuator_control.checkClimate(ERROR_TOLERANCE, setTemp, currTemp) #first number is allowable temp diff. Second number is set temp

	# Update graph
	#Graph_show.updateGraph(setTemp, currTemp)
	
	# Sets delay between reading intervals (should be larger than 5 seconds)
	time.sleep(5)

# Turns off everything at end of experiment
Actuator_control.goodbye()
