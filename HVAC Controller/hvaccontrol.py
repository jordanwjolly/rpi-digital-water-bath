#!/usr/bin/python

########################################################################################################################
#
# RasPi Smart HVAC
# Written by William Thomas - http://willseph.com/
#
########################################################################################################################

# Imports ##############################################################################################################
########################################################################################################################

import os;			# OS functions
import RPi.GPIO as gpio;	# GPIO library
import json;			# JSON library
import time;			# Time functions

# Constants ############################################################################################################
########################################################################################################################

DIR = '/home/pi/thermostat';
SETTINGS_FILE = DIR+'/settings.json';
STATUS_FILE = DIR+'/status.json';
EXCEPTIONS_LOG_FILE = DIR+'/hvaccontrol_exceptions.csv';

# Relay boolean constants. Flipped for Sainsmart relay module.
RELAY_ON = False;
RELAY_OFF = (not RELAY_ON);

TOGGLE_DELAY = 1;
IN_THE_BLIND_TIME = 300; 
COMPRESSOR_RECOVERY_TIME = 60;
COMPRESSOR_STICK_TIME = 60;
FAN_RECOVERY_TIME = 2;

# Relay pins
BOARD_MODE = gpio.BCM;	# The GPIO board mode setting
PIN_FAN = 17;		# Pin for activating the fan.
PIN_COMPRESSOR = 27;	# Pin for compressor unit.
PIN_COOL = 22;		# Pin for "blow direction". On = Cool, Off = Heat.

VER = '0.1';
VERBOSE = True;

# Variables ############################################################################################################
########################################################################################################################

settings = None;
fanOn = False;
heatingOn = False;
coolingOn = False;

lastCompressorDisableTime = 0;
lastCompressorEnableTime = 0;
lastFanDisableTime = 0;
lastSettingsUpdate = 0;

# Functions ############################################################################################################
########################################################################################################################

def goodbye():
	cleanup(); # Cleaning up
	writeStatus();
	writeVerbose('Goodbye!');
	
def cleanup():
	writeVerbose('Running cleanup script...');
	setCooling(False, True);
	setHeating(False, True);
	setFan(False, True); # Turning everything off
#	gpio.cleanup(); # Cleans up GPIO settings
	writeVerbose('Cleanup complete.', True);
	
def delay():
	global TOGGLE_DELAY;
	time.sleep(TOGGLE_DELAY);

def readSettings():
	global SETTINGS_FILE;
	s = None;
	with open(SETTINGS_FILE, 'r') as file:
		s = file.read();
	data = json.loads(s);
	return data;

def setCooling(toggle, force=False):
	global RELAY_ON;
	global RELAY_OFF;
	global PIN_FAN;
	global PIN_COMPRESSOR;
	global PIN_COOL;
	global fanOn;
	global coolingOn;
	global heatingOn;
	global lastCompressorDisableTime;
	global lastCompressorEnableTime;
	global COMPRESSOR_RECOVERY_TIME;
	
	if((not force) and (toggle == coolingOn)):
		writeVerbose('*** Cooling unchanged ('+('on' if coolingOn else 'off')+').',True);
		return;
	
	if(toggle):
		# Cannot enable A/C if fan is off
		if(not (fanOn is True)):
			writeVerbose('*** Cannot enable cooling if fan is disabled!',True);
			return;
			
		# Cannot enable A/C if heating is on
		if(heatingOn):
			writeVerbose('*** Cannot enable cooling if heating is on. Must disable heating first!',True);
			return;
		
		if(int(time.time()) < (lastCompressorDisableTime + COMPRESSOR_RECOVERY_TIME)):
			writeVerbose('*** Cannot enable cooling, compressor in recovery.',True);
			return;
		
		writeVerbose('Enabling cooling...');
		gpio.output(PIN_COMPRESSOR, RELAY_ON);
		gpio.output(PIN_COOL, RELAY_ON);
		coolingOn = True;		
		lastCompressorEnableTime = int(time.time());
		writeVerbose('Cooling enabled.', True);
		
	else:
		writeVerbose('Disabling cooling...');
		gpio.output(PIN_COOL, RELAY_OFF);
		gpio.output(PIN_COMPRESSOR, RELAY_OFF);
		
		if(coolingOn):
			lastCompressorDisableTime = int(time.time());
			
		coolingOn = False;
		writeVerbose('Cooling disabled.', True);
	
	delay();

def setFan(toggle, force=False):
	global RELAY_ON;
	global RELAY_OFF;
	global PIN_FAN;
	global PIN_COMPRESSOR;
	global PIN_COOL;
	global fanOn;
	global coolingOn;
	global heatingOn;
	global lastFanDisableTime;
	global FAN_RECOVERY_TIME;
	
	if((not force) and (toggle == fanOn)):
		writeVerbose('*** Fan unchanged ('+('on' if fanOn else 'off')+').',True);
		return;
	
	if(toggle):
		
		if(int(time.time()) < (lastFanDisableTime + FAN_RECOVERY_TIME)):
			writeVerbose('*** Cannot enable fan, fan in recovery.',True);
			return;
			
		writeVerbose('Enabling fan...');
		gpio.output(PIN_FAN, RELAY_ON);
		fanOn = True;
		writeVerbose('Fan enabled.', True);
		
	else:
		if(coolingOn):
			setCooling(False);
		
		if(heatingOn):
			setHeating(False);
		
		writeVerbose('Disabling fan...');
		gpio.output(PIN_FAN, RELAY_OFF);
		
		if(fanOn):
			lastFanDisableTime = int(time.time());
			
		fanOn = False;
		writeVerbose('Fan disabled.', True); 
		
	delay();

def setHeating(toggle, force=False):
	global RELAY_ON;
	global RELAY_OFF;
	global PIN_FAN;
	global PIN_COMPRESSOR;
	global PIN_COOL;
	global fanOn;
	global coolingOn;
	global heatingOn;
	global lastCompressorEnableTime;
	global lastCompressorDisableTime;
	global COMPRESSOR_RECOVERY_TIME;
	
	if((not force) and (toggle == heatingOn)):
		writeVerbose('*** Heating unchanged ('+('on' if heatingOn else 'off')+').',True);
		return;
	
	if(toggle):
		# Cannot enable heating if fan is off
		if(not (fanOn is True)):
			writeVerbose('*** Cannot enable heating if fan is disabled!',True);
			return;
			
		# Cannot enable heating if A/C is on
		if(coolingOn):
			writeVerbose('*** Cannot enable heating if cooling is on. Must disable cooling first!',True);
			return;
		
		if(int(time.time()) < (lastCompressorDisableTime + COMPRESSOR_RECOVERY_TIME)):
			writeVerbose('*** Cannot enable heating, compressor in recovery.',True);
			return;
		
		writeVerbose('Enabling heating...');
		gpio.output(PIN_COMPRESSOR, RELAY_ON);
		gpio.output(PIN_COOL, RELAY_OFF);
		lastCompressorEnableTime = int(time.time());
		heatingOn = True;
		writeVerbose('Heating enabled.', True);
		
	else:
		writeVerbose('Disabling heating...');
		gpio.output(PIN_COMPRESSOR, RELAY_OFF);
		
		if(heatingOn):
			lastCompressorDisableTime = int(time.time());
			
		heatingOn = False;
		writeVerbose('Heating disabled.', True);
		
	delay();

def setupGPIO():
	global BOARD_MODE;
	global PIN_FAN;
	global PIN_COMPRESSOR;
	global PIN_COOL;
	
	writeVerbose('Setting up GPIO...');
	gpio.setwarnings(False);
	
	# Setting board mode.
	gpio.setmode(BOARD_MODE);
	
	# Setting up output pins
	gpio.setup(PIN_FAN,		gpio.OUT);
	gpio.setup(PIN_COMPRESSOR,	gpio.OUT);
	gpio.setup(PIN_COOL,		gpio.OUT);
	
	gpio.output(PIN_FAN, RELAY_OFF);
	gpio.output(PIN_COMPRESSOR, RELAY_OFF);
	gpio.output(PIN_COOL, RELAY_OFF);
	
	setFan(False, True);	# Setting all relays off.
	setCooling(False, True);
	setHeating(False, True);
	
	writeVerbose('GPIO setup complete.',True);

def writeVerbose(s, newLine=False):
	global VERBOSE;
	
	if(VERBOSE):
		print(s);
		if(newLine is True):
			print('');

def handleInTheBlind():
	# This method checks update times to ensure that the thermostat has not been running too long without
	# being able to receive vital information. If it has, it shuts everything down.
	global IN_THE_BLIND_TIME;
	global lastSettingsUpdate;
	
	t = int(time.time());
	if(t > (IN_THE_BLIND_TIME + lastSettingsUpdate)):
		# Been in the blind for too long, SHUT. DOWN. EVERYTHING.
		setFan(False, True);
		writeVerbose('*** In the blind, disabling circuits.', True);
		return True;
	
	return False;

def checkSensorValidity():
	# This method looks at the settings to check for the "valid" bit.
	# If invalid, everything gets shut down.
	global settings;
	
	if(settings['valid'] is True):
		return True;
	else:
                writeVerbose('*** Settings invalid (In the blind), disabling circuits.', True);
		setFan(False, True);
		return False;

def writeStatus():
	global STATUS_FILE;
	global fanOn;
	global heatingOn;
	global coolingOn;
	global lastCompressorDisableTime;
	global lastCompressorEnableTime;
	global lastSettingsUpdate;
	global lastFanDisableTime;
	
	data = {
		'date': int(time.time()),
		'fan':	fanOn,
		'heating': heatingOn,
		'cooling': coolingOn,
		'lastCompressorDisableTime': lastCompressorDisableTime,
		'lastCompressorEnableTime': lastCompressorEnableTime,
		'lastFanDisableTime': lastFanDisableTime,
		'lastSettingsUpdateTime': lastSettingsUpdate
	};
	with open(STATUS_FILE, 'w') as file:
		file.write(json.dumps(data));

def doMainLoop():
	global TOGGLE_DELAY;
	global settings;
	global coolingOn;
	global heatingOn;
	global lastSettingsUpdate;

	while True:
		# This is the main loop of the HVAC control program
		time.sleep(TOGGLE_DELAY);
		writeStatus();
		t = int(time.time());
		writeVerbose(' ');
		writeVerbose('************************************************************');
		writeVerbose(' ');
		writeVerbose('Main loop... ('+str(t)+')');

		# The first step is to attempt to read data from the SETTINGS_FILE
		try:
			settings = readSettings();
		except:
			# An exception occurred and settings file cannot be reached.
			writeVerbose('Unable to read settings file, checking if in the blind.');
			handleInTheBlind();
			continue;
		
		# At this point, the settings have been read.
		# However we still need to ensure that the last update time isn't out of our emergency range.
		lastSettingsUpdate = settings['date'];
		
		if(handleInTheBlind() is True):
			# Been in the blind for too long, SHUT. DOWN. EVERYTHING.
			continue;
		
		writeVerbose('Settings found.');

		# Confirmed that HVAC Control is in communication with the website.
		# However the sensors themselves may be in the blind.
		if(not checkSensorValidity()):
			continue;

		# Now for the good stuff.		
		# First checking for fan setting. If set to on, then attempt to enable it.
		if(settings['fan_mode'] == 'on'):
			writeVerbose('Fan set to force on, enabling fan.');
			setFan(True);
		else:
			writeVerbose('Fan set to auto.');
		
		# Now we determine what the compressor should be doing.
		# We first check the setting set by the user and go from there
		mode = settings['compressor_mode'];
		if(mode == 'off'):
			writeVerbose('No heat or cool.');
			if(coolingOn):
				setCooling(False);
			if(heatingOn):
				setHeating(False);
			# No compressor, so if the fan is set to "auto", turn it off.
			if(settings['fan_mode'] == 'auto'):
				writeVerbose('Automatic fan disabled.');
				setFan(False);
		else:
			checkClimate(mode);

		# Main loop completed
		writeVerbose('Loop complete.');

def checkClimate(mode):
	global COMPRESSOR_STICK_TIME;
	global settings;
	global heatingOn;
	global coolingOn;	
	global lastCompressorEnableTime;
	
	# This function is called if the compressor is in heat, cool or auto mode.
	# First check the current temperature, set temperature, and threshold.
	
	# If the compressor is in the "stuck" period, just return.
	currentTime = int(time.time());
	if(currentTime < (lastCompressorEnableTime+COMPRESSOR_STICK_TIME)):
		writeVerbose('Compressor currently stuck, so no change.');
		return;
	
	observedTemperature = settings['observed_temperature'];
	setTemperatureMax = settings['temperature_max'];
	setTemperatureMin = settings['temperature_min'];
	threshold = settings['temperature_threshold'];
	if(threshold < 0.5):
		threshold = 0.5;
		writeVerbose('*** Warning: Threshold too low. Setting to 0.5.');
	
	if((setTemperatureMax <= setTemperatureMin) or ((setTemperatureMax-setTemperatureMin) < (threshold*2))):
		writeVerbose('*** Error: Overlap between set minimum and maximum temperatures.');
		return;
	
	writeVerbose('Current temperature: '+str(observedTemperature)+' F');
	writeVerbose('Set minimum temperature: '+str(setTemperatureMin)+' F');
	writeVerbose('Set maximum temperature: '+str(setTemperatureMax)+' F');
	writeVerbose('');
	
	# The A/C (and fan) should be enabled if the observed temperature is warmer than
	# the set temperature, plus the threshold
	
	hotterThanMax = False;
	coolerThanMin = False;
	
	# Checking to see if it's warmer than the high range (ie. if the A/C should turn on)
	# If the A/C is on right now, it should stay on until it goes past the threshold
	if(coolingOn and (setTemperatureMax < (observedTemperature+threshold))):
		hotterThanMax = True;
	# If the A/C is not on right now, it should turn on when it hits the threshold
	if((not coolingOn) and (setTemperatureMax < (observedTemperature-threshold))):
		hotterThanMax = True;

	# Checking to see if it's colder than the low range (ie. if the heater should turn on)
	# If the heater is on right now, it should stay on until it goes past the threshold
	if(heatingOn and (setTemperatureMin > (observedTemperature-threshold))):
		coolerThanMin = True;
	# If the heater is not on right now, it should turn on when it hits the threshold
	if((not heatingOn) and (setTemperatureMin > (observedTemperature+threshold))):
		coolerThanMin = True;

	
	if(hotterThanMax and coolerThanMin):
		writeVerbose('*** Error: Outside of both ranges somehow.');
		return;
	
	if((not hotterThanMax) and (not coolerThanMin)):
		writeVerbose('Temperature is in range, so no compressor necessary.');
		setHeating(False);
		setCooling(False);
		if(settings['fan_mode']=='auto'):
			setFan(False);
	
	elif(hotterThanMax and (mode == 'cool' or mode == 'auto')):
		writeVerbose('Temperature is too warm and A/C is enabled, activating A/C.');
		setFan(True);
		if(heatingOn):
			setHeating(False);
		setCooling(True);

	elif(coolerThanMin and (mode == 'heat' or mode == 'auto')):
		writeVerbose('Temperature is too cold and heating is enabled, activating heater.');
		setFan(True);
		if(coolingOn):
			setCooling(False);
		setHeating(True);

def logException(e):
	global EXCEPTIONS_LOG_FILE;
	
	line = str(int(time.time()))+','+str(e);
	with open(EXCEPTIONS_LOG_FILE, 'a') as file:
		file.write(line);

# Main #################################################################################################################
########################################################################################################################

#os.system('clear'); # Clears the terminal

setupGPIO(); # Setting up GPIO
writeStatus();

# Resetting fan and compressor times
lastCompressorDisableTime = 0;
lastFanDisableTime = 0;

try:
	doMainLoop();

except KeyboardInterrupt:
	pass;

except Exception, e:
	writeVerbose('Exception occurred!!!', True);
	writeVerbose(str(e), True);
	logException(e);
	pass;

goodbye();
