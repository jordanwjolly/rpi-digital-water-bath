#!/usr/bin/python

#This file dictates what the heating profile looks like
import time;			# Time functions
import actuator_control as actuator

#Sets up everything
actuator.setupGPIO(); 

#Range of time
for t in range(0, 1000):

	#The Equation
	setTemp = 20+float(t)/2
	
	#Does all of the stuff
	actuator.checkClimate(0.1, setTemp) #first number is allowable temp diff. Second number is set temp
	
	#Sets delay between reading intervals (should be larger than 5 seconds)
	time.sleep(5)

#Turns off everything at end of experiment
actuator.goodbye();