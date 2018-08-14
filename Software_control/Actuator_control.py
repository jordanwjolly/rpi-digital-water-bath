#!/usr/bin/python

# Imports ##############################################################################################################
########################################################################################################################

import os;			# OS functions
import RPi.GPIO as gpio;	# GPIO library
import json;			# JSON library
import time;			# Time functions
import subprocess
import pickle
import numpy as np

# Constants ############################################################################################################
########################################################################################################################
#Save path of current temperature
DIR = dir_path = os.path.dirname(os.path.realpath(__file__))
CURRENT_FILE = DIR+'/SensorValues.txt'

TOGGLE_DELAY = 1;
COOLER_RECOVERY_TIME = 60;
HEATER_RECOVERY_TIME = 10; 	#Time out between turning it off/on again
TEMP_THRESHOLD = 0.1; 					#Allowable difference in measured temp vs desired temp

# Relay pins
BOARD_MODE = gpio.BOARD;	# The GPIO board mode setting
PIN_HEAT = 38;	# Pin for heat unit.
PIN_COOL = 40;		# Pin for "cooler

VER = '0.1';
VERBOSE = True;

# Variables ############################################################################################################
########################################################################################################################

settings = None;
heatingOn = False;
coolingOn = False;

lastCoolerDisableTime = 0;
lastCoolerEnableTime = 0;
lastHeaterDisableTime = 0;
lastHeaterEnableTime = 0;

# Functions ############################################################################################################
########################################################################################################################

def goodbye():
	cleanup(); # Cleaning up
	print('Goodbye!');
	
def cleanup():
	print('Running cleanup script...');
	#setCooling(False, True);
	setHeating(False, True);
	print('Cleanup complete.');
	
def delay():
	global TOGGLE_DELAY;
	time.sleep(TOGGLE_DELAY);

#TURNS ON THE COOLER
def setCooling(toggle, force=False):
	global coolingOn;
	global heatingOn;
	global lastCoolerDisableTime;
	global lastCoolerEnableTime;
	global COOLER_RECOVERY_TIME;
	
	#Checking to see if keep cooling on
	if((not force) and (toggle == coolingOn)):
		print('*** Cooling stays on ***');
		return;
	
	#Checking to see if change
	if(toggle):
		# Cannot enable A/C if heating is on
		if(heatingOn):
			print('*** Cannot enable cooling if heating is on. Must disable heating first!');
			return;
		
		if(int(time.time()) < (lastCoolerDisableTime + COOLER_RECOVERY_TIME)):
			print('*** Cannot enable cooling, cooler in recovery ***');
			return;
		
		print('Enabling cooling...');
		gpio.output(PIN_COOL, True);
		coolingOn = True;		
		lastCoolerEnableTime = int(time.time());
		print('*** Cooling enabled ***');
		
	else:
		print('Disabling cooling...');
		gpio.output(PIN_COOL, False);
		
		if(coolingOn):
			lastCoolerDisableTime = int(time.time());
			
		coolingOn = False;
		print('*** Cooling disabled ***');
	
	delay();

#TURNS ON THE HEATER
def setHeating(toggle, DIR, relayID):

	global heatingOn
	global lastHeaterEnableTime
	global lastHeaterDisableTime
	global HEATER_RECOVERY_TIME
	
	if(toggle == heatingOn):
		print('*** Heating stays on***');
		return;
	
	#Checking to see if change
	if(toggle):
		
		# Cannot enable heating if A/C is on
		if(coolingOn):
			#print('*** Cannot enable heating if cooling is on. Must disable cooling first! ***')
			return
		
		if(int(time.time()) < (lastHeaterDisableTime + HEATER_RECOVERY_TIME)):
			print('*** Cannot enable heating, heater in recovery ***')
			return;
		
		#print('Enabling heating...')
		gpio.output(PIN_HEAT, True)
		subprocess.call([DIR + "/Hardware_control/WTI_on.sh", str(relayID)])
		delay()
		lastHeaterEnableTime = int(time.time())
		heatingOn = True
		print('*** Heating enabled ***')
		
	else:
		#print('Disabling heating...')
		gpio.output(PIN_HEAT, False)
		subprocess.call([DIR + "/Hardware_control/WTI_off.sh", str(relayID)])  #Calls bash script to turn heating on
		delay()
		
		if(heatingOn):
			lastHeaterDisableTime = int(time.time())
			
		heatingOn = False;
		print('*** Heating disabled ***')
		
	delay();

def setupGPIO():
	global BOARD_MODE
	global PIN_HEAT
	global PIN_COOL
	
	print('\nSetting up GPIO... \n')
	gpio.setwarnings(False)
	
	# Setting board mode.
	gpio.setmode(BOARD_MODE)
	
	# Setting up output pins
	gpio.setup(PIN_HEAT,	gpio.OUT)
	gpio.setup(PIN_COOL,		gpio.OUT)
	
	gpio.output(PIN_HEAT, True)
	gpio.output(PIN_COOL, True)
	
	print("Initially turn all systems off....\n")
	#setCooling(False, True)
	setHeating(False, True, 0)

	print('\nGPIO setup complete\n****************************************');






def currTemp(CURRENT_TEMP_FILE ):
	#Gets sensor value, returns current temperature
	#print("\nReading current temperature")
	#s = None
	#with open(CURRENT_FILE) as file:
		#s = file.read()
		#data = json.loads(s)
        #return (data['date'], data['temperature']);
	#currTemp = data['temperature']
	currTemp= pickle.load(open(CURRENT_TEMP_FILE , 'r'))
	return currTemp






def checkClimate(setTemp, currTemp , threshold, DIR, relayID):
	global heatingOn
	global coolingOn
	global lastCoolerEnableTime
	global lastHeaterEnableTime

	#print("Set-point Temperature is: " + str(setTemp))
	#print("Current Temperature is: " + str(currTemp))
	print('\nTesting Tank: ' + str(relayID))
	
	if(threshold < TEMP_THRESHOLD ):
		threshold = TEMP_THRESHOLD
		print('*** Warning: Threshold too low. Setting to 0.1.')
	
	hotterThanSet = False;
	coolerThanSet = False;
	
	# CHECKING TO SEE IF TEMP IS ABOVE/BELOW SET POINT
	# COOLER: Cooler is on, it should stay on until it goes past the threshold
	if(coolingOn and (setTemp< (currTemp+threshold))):
		hotterThanSet = True;
	# COOLER: Cooler is currently off, it should turn on when it hits the threshold
	if((not coolingOn) and (setTemp< (currTemp-threshold))):
		hotterThanSet = True;
	# HEATER: Heater is on, it should stay on until it goes past the threshold
	if(heatingOn and (setTemp> (currTemp-threshold))):
		coolerThanSet = True;
	# HEATER: Heater is currently off, it should turn on when it hits the threshold
	if((not heatingOn) and (setTemp> (currTemp+threshold))):
		coolerThanSet = True;

	# TURN THE HEATER/COOLER ON/OFF
	if(hotterThanSet and coolerThanSet):
		#print('*** Error: Outside of both ranges somehow.');
		return;
	
	if((not hotterThanSet) and (not coolerThanSet)):
		#print('Temperature is in range, no actuation required');
		print("Current: " + str(currTemp) + " Set-point: " + str(setTemp) + " Heating: OFF")
		setHeating(False, DIR, relayID);
		
		#setCooling(False);
	
	elif(hotterThanSet):
		#print('Water temperature is too warm');
		print("Current: " + str(currTemp) + " Set-point: " + str(setTemp) + " Heating: OFF")
		if(heatingOn):
			setHeating(False, DIR, relayID);
		#setCooling(True);
		
		#else:
			#print("*** Heating is off ***")

	elif(coolerThanSet):
		#print('Water temperature is too cold');
		#if(coolingOn):
			#setCooling(False);
		print("Current: " + str(currTemp) + " Set-point: " + str(setTemp) + " Heating: ON")
		setHeating(True, DIR, relayID);
		


