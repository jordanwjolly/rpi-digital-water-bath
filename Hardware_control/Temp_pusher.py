#!/usr/bin/python

######################################################################################################
# TempPusher.py
# Uses the logged current.json to update the website via the API with current climate information
######################################################################################################

# Imports ############################################################################################

import sys;
import time;
import json;
import requests;

# Constants ##########################################################################################

DIR = '/home/pi/thermostat';
CURRENT_FILE = DIR+'/current.json';
PAUSE_INTERVAL = 5;
UPDATE_URL = "https://XXXXX/rpi/update_sensor.php"; # Replace with your remote URL
VERBOSE = True;

SENSOR_ID = "XXXXX"; # Change this to your public sensor ID.
SENSOR_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"; # Change this to your private sensor key. 

# Variables ##########################################################################################

# Functions ##########################################################################################

def getCurrent():
	global CURRENT_FILE;
        s = None;
        with open(CURRENT_FILE) as file:
                s = file.read();
        data = json.loads(s);
        return (data['date'], data['temperature']);

def sendUpdate(temperature, date):
	global UPDATE_URL;
	global SENSOR_ID;
	global SENSOR_KEY;
	
	payload = {
		'id':		SENSOR_ID,
		'key':		SENSOR_KEY,
		'temperature':	temperature,
		'time':		date
	};
	try:
		resp = requests.post(UPDATE_URL, data=payload);
		data = json.loads(resp.text);
		if(data["success"] is True):
			return True;
	except:
		return False;

def writeVerbose(str, newline = False):
	global VERBOSE;
	if(not VERBOSE):
		return;
	print(str);
	if(newline):
		print(' ');

# Main ###############################################################################################

writeVerbose('Beginning updater script.');
writeVerbose('Press Ctrl+C to stop loop.', True);

while(True):
	try:
		date, temperature = getCurrent();
	except:
		writeVerbose('Could not fetch current climate data.');
		time.sleep(1);
		continue;
	writeVerbose('Updating temperature...');
	if(sendUpdate(temperature, date)):
		writeVerbose('Update successful!');
	else:
		writeVerbose('Update failed.');
	writeVerbose(' ');
	time.sleep(PAUSE_INTERVAL);

writeVerbose(' ');
writeVerbose('Updater closing, goodbye.', True);
