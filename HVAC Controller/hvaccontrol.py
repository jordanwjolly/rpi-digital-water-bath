#!/usr/bin/python

#NOTES: The state machine is a little bit wack. Currently correctly identifies cold/hot incorrectly, but then actuates correctly according to the wrong 
#						Identification. There is a bunch of things going weird with the t-1 t0 logic, i reckon simplify the 


# Imports ##############################################################################################################
########################################################################################################################

import os;			# OS functions
import RPi.GPIO as gpio;	# GPIO library
import json;			# JSON library
import time;			# Time functions

# Constants ############################################################################################################
########################################################################################################################

# Relay boolean constants. Flipped for Sainsmart relay module.
RELAY_ON = False;
RELAY_OFF = (not RELAY_ON);

TOGGLE_DELAY = 1;
COOLER_RECOVERY_TIME = 60;
HEATER_RECOVERY_TIME = 60;

# Relay pins
BOARD_MODE = gpio.BOARD;	# The GPIO board mode setting
PIN_HEAT = 38;	# Pin for heat unit.
PIN_COOL = 40;		# Pin for "blow direction". On = Cool, Off = Heat.

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
	setCooling(False, True);
	setHeating(False, True);
	print('Cleanup complete.');
	
def delay():
	global TOGGLE_DELAY;
	time.sleep(TOGGLE_DELAY);

#TURNS ON THE COOLER
def setCooling(toggle, force=False):
	global RELAY_ON;
	global RELAY_OFF;
	global PIN_HEAT;
	global PIN_COOL;
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
		gpio.output(PIN_COOL, RELAY_ON);
		coolingOn = True;		
		lastCoolerEnableTime = int(time.time());
		print('*** Cooling enabled ***');
		
	else:
		print('Disabling cooling...');
		gpio.output(PIN_COOL, RELAY_OFF);
		
		if(coolingOn):
			lastCoolerDisableTime = int(time.time());
			
		coolingOn = False;
		print('*** Cooling disabled ***');
	
	delay();

#TURNS ON THE HEATER
def setHeating(toggle, force=False):
	global RELAY_ON;
	global RELAY_OFF;
	global PIN_FAN;
	global PIN_HEAT;
	global PIN_COOL;
	global fanOn;
	global coolingOn;
	global heatingOn;
	global lastHeaterEnableTime;
	global lastHeaterDisableTime;
	global HEATER_RECOVERY_TIME;
	
	if((not force) and (toggle == heatingOn)):
		print('*** Heating stays on***');
		return;
	
	#Checking to see if change
	if(toggle):
		
		# Cannot enable heating if A/C is on
		if(coolingOn):
			print('*** Cannot enable heating if cooling is on. Must disable cooling first! ***');
			return;
		
		if(int(time.time()) < (lastHeaterDisableTime + HEATER_RECOVERY_TIME)):
			print('*** Cannot enable heating, heater in recovery ***');
			return;
		
		print('Enabling heating...');
		gpio.output(PIN_HEAT, RELAY_ON);
		lastHeaterEnableTime = int(time.time());
		heatingOn = True;
		print('*** Heating enabled ***');
		
	else:
		print('Disabling heating...');
		gpio.output(PIN_HEAT, RELAY_OFF);
		
		if(heatingOn):
			lastHeaterDisableTime = int(time.time());
			
		heatingOn = False;
		print('*** Heating disabled ***');
		
	delay();

def setupGPIO():
	global BOARD_MODE;
	global PIN_HEAT;
	global PIN_COOL;
	
	print('\nSetting up GPIO... \n');
	gpio.setwarnings(False);
	
	# Setting board mode.
	gpio.setmode(BOARD_MODE);
	
	# Setting up output pins
	gpio.setup(PIN_HEAT,	gpio.OUT);
	gpio.setup(PIN_COOL,		gpio.OUT);
	
	gpio.output(PIN_HEAT, RELAY_OFF);
	gpio.output(PIN_COOL, RELAY_OFF);
	
	print("Initially turn all systems off....\n")
	setCooling(False, True);
	setHeating(False, True);
	
	print('\nGPIO setup complete\n****************************************');

def getcurrTemp():
	global currTemp;
	#Gets sensor value, returns current temperature
	print("\nReading current temperature")	
	currTemp = 25;
	print("Current Temperature is: " + str(currTemp))
	return;

def checkClimate(threshold):
	global currTemp;
	global setTempNow
	global setTempLast
	global heatingOn;
	global coolingOn;	
	global lastCoolerEnableTime;
	global lastHeaterEnableTime;
	
	getcurrTemp()
	print("Set-point Temperature is: " + str(setTempNow))
	
	if(threshold < 0.5):
		threshold = 0.5;
		print('*** Warning: Threshold too low. Setting to 0.5.');
	
	hotterThanSet = False;
	coolerThanSet = False;
	
	# CHECKING TO SEE IF TEMP IS ABOVE/BELOW SET POINT
	# COOLER: Cooler is on, it should stay on until it goes past the threshold
	if(coolingOn and (setTempNow< (currTemp+threshold))):
		hotterThanSet = True;
		print(1)
	# COOLER: Cooler is currently off, it should turn on when it hits the threshold
	if((not coolingOn) and (setTempNow< (currTemp-threshold))):
		hotterThanSet = True;
		print(2)
	# HEATER: Heater is on, it should stay on until it goes past the threshold
	if(heatingOn and (setTempNow> (currTemp-threshold))):
		coolerThanSet = True;
		print(3)
	# HEATER: Heater is currently off, it should turn on when it hits the threshold
	if((not heatingOn) and (setTempNow> (currTemp+threshold))):
		coolerThanSet = True;
		print(4)

	# TURN THE HEATER/COOLER ON/OFF
	if(hotterThanSet and coolerThanSet):
		print('*** Error: Outside of both ranges somehow.');
		return;
	
	if((not hotterThanSet) and (not coolerThanSet)):
		print('Temperature is in range, no actuation required');
		setHeating(False);
		setCooling(False);
	
	elif(hotterThanSet):
		print('Temperature is too warm');
		if(heatingOn):
			setHeating(False);
		setCooling(True);

	elif(coolerThanSet):
		print('Temperature is too cold');
		if(coolingOn):
			setCooling(False);
		setHeating(True);


# Main #################################################################################################################
########################################################################################################################

setupGPIO(); # Setting up GPIO

# Resetting fan and compressor times
lastCoolerDisableTime = 0;
lastFanDisableTime = 0;

global setTempNow

while(True):

	setTempNow=30
	checkClimate(0.5)
	time.sleep(1)
	setTempNow=30
	checkClimate(0.5)
	time.sleep(1)
	setTempNow=24	
	checkClimate(0.5)
	time.sleep(1)
	setTempNow=26
	checkClimate(0.5)
	time.sleep(1)
	setTempNow=20	
	checkClimate(0.5)
	time.sleep(1)
	setTempNow=20
	checkClimate(0.5)
	time.sleep(1)


goodbye();
