#!/usr/bin/python

########################################################################################################################
#
# RasPi Smart HVAC Cleanup script
# Written by William Thomas - http://willseph.com/
#
########################################################################################################################

# Imports ##############################################################################################################
########################################################################################################################

import os;			# OS functions
import RPi.GPIO as gpio;	# GPIO library
import json;			# JSON library
import time;			# Time functions
import atexit;			# Cleanup function registrar

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
IN_THE_BLIND_TIME = (60 * 10); 
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

# Main #################################################################################################################
########################################################################################################################

#os.system('clear'); # Clears the terminal

setupGPIO(); # Setting up GPIO
goodbye();
