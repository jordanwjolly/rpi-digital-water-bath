#!/usr/bin/python

# Imports ##############################################################################################################
########################################################################################################################

import os;			# OS functions
import RPi.GPIO as gpio;	# GPIO library
import json;			# JSON library
import time;			# Time functions

# Constants ############################################################################################################
########################################################################################################################

#DIR = '/home/pi/thermostat';
#SETTINGS_FILE = DIR+'/settings.json';
#STATUS_FILE = DIR+'/status.json';
#EXCEPTIONS_LOG_FILE = DIR+'/hvaccontrol_exceptions.csv';

# Relay boolean constants. Flipped for Sainsmart relay module.
RELAY_ON = False;
RELAY_OFF = (not RELAY_ON);

TOGGLE_DELAY = 1;
IN_THE_BLIND_TIME = 300; 
COOLER_RECOVERY_TIME = 60;
HEATER_RECOVERY_TIME = 60;
COMPRESSOR_STICK_TIME = 60;
#FAN_RECOVERY_TIME = 2;

# Relay pins
BOARD_MODE = gpio.BOARD;	# The GPIO board mode setting
PIN_HEAT = 38;	# Pin for heat unit.
PIN_COOL = 40;		# Pin for "blow direction". On = Cool, Off = Heat.

VER = '0.1';
VERBOSE = True;

# Variables ############################################################################################################
########################################################################################################################

settings = None;
#fanOn = False;
heatingOn = False;
coolingOn = False;

lastCoolerDisableTime = 0;
lastCoolerEnableTime = 0;
lastHeaterDisableTime = 0;
lastHeaterEnableTime = 0;
#lastFanDisableTime = 0;
#lastSettingsUpdate = 0;

# Functions ############################################################################################################
########################################################################################################################

def goodbye():
	cleanup(); # Cleaning up
	print('Goodbye!');
	
def cleanup():
	print('Running cleanup script...');
	setCooling(False, True);
	setHeating(False, True);
#	setFan(False, True); # Turning everything off
#	gpio.cleanup(); # Cleans up GPIO settings
	print('Cleanup complete.', True);
	
def delay():
	global TOGGLE_DELAY;
	time.sleep(TOGGLE_DELAY);

#def readSettings():
#	global SETTINGS_FILE;
#	s = None;
#	with open(SETTINGS_FILE, 'r') as file:
#		s = file.read();
#	data = json.loads(s);
#	return data;

def setCooling(toggle, force=False):
	global RELAY_ON;
	global RELAY_OFF;
	#global PIN_FAN;
	global PIN_HEAT;
	global PIN_COOL;
	#global fanOn;
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
#		# Cannot enable A/C if fan is off
#		if(not (fanOn is True)):
#			print('*** Cannot enable cooling if fan is disabled!',True);
#			return;
			
		# Cannot enable A/C if heating is on
		#This could change in version 2.0
		if(heatingOn):
			print('*** Cannot enable cooling if heating is on. Must disable heating first!');
			return;
		
		if(int(time.time()) < (lastCoolerDisableTime + COOLER_RECOVERY_TIME)):
			print('*** Cannot enable cooling, cooler in recovery.',True);
			return;
		
		print('Enabling cooling...');
		#gpio.output(PIN_HEAT, RELAY_ON);
		gpio.output(PIN_COOL, RELAY_ON);
		coolingOn = True;		
		lastCoolerEnableTime = int(time.time());
		print('Cooling enabled.', True);
		
	else:
		print('Disabling cooling...');
		gpio.output(PIN_COOL, RELAY_OFF);
		#gpio.output(PIN_HEAT, RELAY_OFF);
		
		if(coolingOn):
			lastCoolerDisableTime = int(time.time());
			
		coolingOn = False;
		print('Cooling disabled.', True);
	
	delay();

#def setFan(toggle, force=False):
#	global RELAY_ON;
#	global RELAY_OFF;
#	global PIN_FAN;
#	global PIN_HEAT;
#	global PIN_COOL;
#	global fanOn;
#	global coolingOn;
#	global heatingOn;
#	global lastFanDisableTime;
#	global FAN_RECOVERY_TIME;
#	
#	if((not force) and (toggle == fanOn)):
#		print('*** Fan unchanged ('+('on' if fanOn else 'off')+').',True);
#		return;
#	
#	if(toggle):
#		
#		if(int(time.time()) < (lastFanDisableTime + FAN_RECOVERY_TIME)):
#			print('*** Cannot enable fan, fan in recovery.',True);
#			return;
#			
#		print('Enabling fan...');
#		gpio.output(PIN_FAN, RELAY_ON);
#		fanOn = True;
#		print('Fan enabled.', True);
#		
#	else:
#		if(coolingOn):
#			setCooling(False);
#		
#		if(heatingOn):
#			setHeating(False);
#		
#		print('Disabling fan...');
#		gpio.output(PIN_FAN, RELAY_OFF);
#		
#		if(fanOn):
#			lastFanDisableTime = int(time.time());
#			
#		fanOn = False;
#		print('Fan disabled.', True); 
#		
#	delay();

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
		print('*** Heating unchanged ***');
		return;
	
#	if(toggle):
#		# Cannot enable heating if fan is off
#		if(not (fanOn is True)):
#			print('*** Cannot enable heating if fan is disabled!',True);
#			return;
			
		# Cannot enable heating if A/C is on
		if(coolingOn):
			print('*** Cannot enable heating if cooling is on. Must disable cooling first!');
			return;
		
		if(int(time.time()) < (lastHeaterDisableTime + HEATER_RECOVERY_TIME)):
			print('*** Cannot enable heating, compressor in recovery.');
			return;
		
		print('Enabling heating...');
		gpio.output(PIN_HEAT, RELAY_ON);
#		gpio.output(PIN_COOL, RELAY_OFF);
		lastHeaterEnableTime = int(time.time());
		heatingOn = True;
		print('Heating enabled.', True);
		
	else:
		print('Disabling heating...');
		gpio.output(PIN_HEAT, RELAY_OFF);
		
		if(heatingOn):
			lastHeaterDisableTime = int(time.time());
			
		heatingOn = False;
		print('Heating disabled.', True);
		
	delay();

def setupGPIO():
	global BOARD_MODE;
#	global PIN_FAN;
	global PIN_HEAT;
	global PIN_COOL;
	
	print('Setting up GPIO...');
	gpio.setwarnings(False);
	
	# Setting board mode.
	gpio.setmode(BOARD_MODE);
	
	# Setting up output pins
	#gpio.setup(PIN_FAN,		gpio.OUT);
	gpio.setup(PIN_HEAT,	gpio.OUT);
	gpio.setup(PIN_COOL,		gpio.OUT);
	
	#gpio.output(PIN_FAN, RELAY_OFF);
	gpio.output(PIN_HEAT, RELAY_OFF);
	gpio.output(PIN_COOL, RELAY_OFF);
	
	#setFan(False, True);	# Setting all relays off.
	setCooling(False, True);
	setHeating(False, True);
	
	print('GPIO setup complete.',True);

#def print(s, newLine=False):
#	global VERBOSE;
#	
#	if(VERBOSE):
#		print(s);
#		if(newLine is True):
#			print('');

#def handleInTheBlind():
#	# This method checks update times to ensure that the thermostat has not been running too long without
#	# being able to receive vital information. If it has, it shuts everything down.
#	global IN_THE_BLIND_TIME;
#	global lastSettingsUpdate;
#	
#	t = int(time.time());
#	if(t > (IN_THE_BLIND_TIME + lastSettingsUpdate)):
#		# Been in the blind for too long, SHUT. DOWN. EVERYTHING.
#		setFan(False, True);
#		print('*** In the blind, disabling circuits.', True);
#		return True;
#	
#	return False;
#
#def checkSensorValidity():
#	# This method looks at the settings to check for the "valid" bit.
#	# If invalid, everything gets shut down.
#	global settings;
#	
#	if(settings['valid'] is True):
#		return True;
#	else:
#                print('*** Settings invalid (In the blind), disabling circuits.');
#		#setFan(False, True);
#		return False;

#def writeStatus():
#	global STATUS_FILE;
#	global fanOn;
#	global heatingOn;
#	global coolingOn;
#	global lastCoolerDisableTime;
#	global lastCoolerEnableTime;
#	global lastSettingsUpdate;
#	global lastFanDisableTime;
#	
#	data = {
#		'date': int(time.time()),
#		'fan':	fanOn,
#		'heating': heatingOn,
#		'cooling': coolingOn,
#		'lastCoolerDisableTime': lastCoolerDisableTime,
#		'lastCoolerEnableTime': lastCoolerEnableTime,
#		'lastFanDisableTime': lastFanDisableTime,
#		'lastSettingsUpdateTime': lastSettingsUpdate
#	};
#	with open(STATUS_FILE, 'w') as file:
#		file.write(json.dumps(data));

#def doMainLoop():
#	global TOGGLE_DELAY;
#	global settings;
#	global coolingOn;
#	global heatingOn;
#	global lastSettingsUpdate;
#
#	while True:
#		# This is the main loop of the HVAC control program
#		time.sleep(TOGGLE_DELAY);
##		writeStatus();
#		t = int(time.time());
#		print(' ');
#		print('************************************************************');
#		print(' ');
#		print('Main loop... ');
#
#		# The first step is to attempt to read data from the SETTINGS_FILE
#		try:
#			settings = readSettings();
#		except:
#			# An exception occurred and settings file cannot be reached.
#			print('Unable to read settings file, checking if in the blind.');
#			handleInTheBlind();
#			continue;
#		
#		# At this point, the settings have been read.
#		# However we still need to ensure that the last update time isn't out of our emergency range.
#		lastSettingsUpdate = settings['date'];
#		
#		if(handleInTheBlind() is True):
#			# Been in the blind for too long, SHUT. DOWN. EVERYTHING.
#			continue;
#		
#		print('Settings found.');
#
#		# Confirmed that HVAC Control is in communication with the website.
#		# However the sensors themselves may be in the blind.
#		if(not checkSensorValidity()):
#			continue;
#
#		# Now for the good stuff.		
#		# First checking for fan setting. If set to on, then attempt to enable it.
#		if(settings['fan_mode'] == 'on'):
#			print('Fan set to force on, enabling fan.');
#			setFan(True);
#		else:
#			print('Fan set to auto.');
#		
#		# Now we determine what the compressor should be doing.
#		# We first check the setting set by the user and go from there
#		mode = settings['compressor_mode'];
#		if(mode == 'off'):
#			print('No heat or cool.');
#			if(coolingOn):
#				setCooling(False);
#			if(heatingOn):
#				setHeating(False);
#			# No compressor, so if the fan is set to "auto", turn it off.
#			if(settings['fan_mode'] == 'auto'):
#				print('Automatic fan disabled.');
#				setFan(False);
#		else:
#			checkClimate(mode);
#
#		# Main loop completed
#		print('Loop complete.');

def getCurrentTemp():
	global currentTemp;
	#Gets sensor value, returns current temperature
	print("\nReading current temperature")	
	currentTemp = 25;
	print("Current Temperature is: " + str(currentTemp))
	return;

def checkClimate(setTemperature, threshold):
	global COMPRESSOR_STICK_TIME;
	global currentTemp;
	global heatingOn;
	global coolingOn;	
	global lastCoolerEnableTime;
	global lastHeaterEnableTime;
	
	# This function is called if the compressor is in heat, cool or auto mode.
	# First check the current temperature, set temperature, and threshold.
	
	# If the compressor is in the "stuck" period, just return.
	currentTime = int(time.time());
	if(currentTime < (lastHeaterEnableTime+COMPRESSOR_STICK_TIME)):
		print('Heater currently stuck, so no change.');
		return;
		
	if(currentTime < (lastCoolerEnableTime+COMPRESSOR_STICK_TIME)):
		print('Cooler currently stuck, so no change.');
		return;
	
	getCurrentTemp()
#	observedTemperature = settings['observed_temperature'];
#	setTemperatureMax = settings['temperature_max'];
#	setTemperatureMin = settings['temperature_min'];
#	threshold = settings['temperature_threshold'];
	if(threshold < 0.5):
		threshold = 0.5;
		print('*** Warning: Threshold too low. Setting to 0.5.');
	
#	if((setTemperatureMax <= setTemperatureMin) or ((setTemperatureMax-setTemperatureMin) < (threshold*2))):
#		print('*** Error: Overlap between set minimum and maximum temperatures.');
#		return;
	
#	print('Current temperature: '+str(observedTemperature)+' F');
#	print('Set minimum temperature: '+str(setTemperatureMin)+' F');
#	print('Set maximum temperature: '+str(setTemperatureMax)+' F');
#	print('');
	
	# The A/C (and fan) should be enabled if the observed temperature is warmer than
	# the set temperature, plus the threshold
	
	hotterThanMax = False;
	coolerThanMin = False;
	
	#CHECKING FOR COOLER
	# Checking to see if it's warmer than the high range (ie. if the A/C should turn on)
	# If the A/C is on right now, it should stay on until it goes past the threshold
	if(coolingOn and (setTemperature < (currentTemp+threshold))):
		hotterThanMax = True;
	# If the A/C is not on right now, it should turn on when it hits the threshold
	if((not coolingOn) and (setTemperature < (currentTemp-threshold))):
		hotterThanMax = True;

	#CHECKING FOR HEATER
	# Checking to see if it's colder than the low range (ie. if the heater should turn on)
	# If the heater is on right now, it should stay on until it goes past the threshold
	if(heatingOn and (setTemperature > (currentTemp-threshold))):
		coolerThanMin = True;
	# If the heater is not on right now, it should turn on when it hits the threshold
	if((not heatingOn) and (setTemperature > (currentTemp+threshold))):
		coolerThanMin = True;

	
	if(hotterThanMax and coolerThanMin):
		print('*** Error: Outside of both ranges somehow.');
		return;
	
	if((not hotterThanMax) and (not coolerThanMin)):
		print('Temperature is in range, so no compressor necessary.');
		setHeating(False);
		setCooling(False);
		#if(settings['fan_mode']=='auto'):
#			setFan(False);
	
	elif(hotterThanMax):
		print('Temperature is too warm and A/C is enabled, activating A/C.');
		#setFan(True);
		if(heatingOn):
			setHeating(False);
		setCooling(True);

	elif(coolerThanMin):
		print('Temperature is too cold and heating is enabled, activating heater.');
		#setFan(True);
		if(coolingOn):
			setCooling(False);
		setHeating(True);

#def logException(e):
#	global EXCEPTIONS_LOG_FILE;
#	
#	line = str(int(time.time()))+','+str(e);
#	with open(EXCEPTIONS_LOG_FILE, 'a') as file:
#		file.write(line);

# Main #################################################################################################################
########################################################################################################################

#os.system('clear'); # Clears the terminal

setupGPIO(); # Setting up GPIO
#writeStatus();

# Resetting fan and compressor times
lastCoolerDisableTime = 0;
lastFanDisableTime = 0;

while(True):
	checkClimate(30, 0.5)
	time.sleep(10)
	checkClimate(25, 0.5)
	time.sleep(10)
	checkClimate(20, 0.5)
	time.sleep(10)


#except KeyboardInterrupt:
#	pass;
#
#except Exception, e:
#	print('Exception occurred!!!', True);
#	print(str(e), True);
#	logException(e);
#	pass;

goodbye();
