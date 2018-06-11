#!/usr/bin/python

######################################################################################################
# Puller.py
# Pulls down information from the database to use for HVAC controls.
######################################################################################################

# Imports ############################################################################################

import sys;
import time;
import json;
import requests;

# Constants ##########################################################################################

DIR = '/home/pi/thermostat';
SETTINGS_FILE = DIR+'/settings.json';
PAUSE_INTERVAL = 1;
PULL_URL = "https://XXXXXX/rpi/get_settings.php"; # Replace with your remote URL
VERBOSE = True;

# Variables ##########################################################################################

# Functions ##########################################################################################

def writeSettings(data):
	global SETTINGS_FILE;
	data['date'] = int(time.time());
	with open(SETTINGS_FILE, 'w') as file:
		file.write(json.dumps(data));

def getSettings():
	global PULL_URL;
	
	data = None;
	try:
		resp = requests.get(PULL_URL, data={});
		data = json.loads(resp.text);
		if(not (data["success"] is True)):
			return False;
	except:
		return False;
	
	try:
		return data['data'];
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

writeVerbose('Beginning puller script.');
writeVerbose('Press Ctrl+C to stop loop.', True);

while(True):
	writeVerbose('Pulling settings...');
	settings = getSettings();
	if(settings):
		writeVerbose(json.dumps(settings));
		writeSettings(settings);
	else:
		writeVerbose('Pull failed.');
	writeVerbose(' ');
	time.sleep(PAUSE_INTERVAL);

writeVerbose(' ');
writeVerbose('Puller closing, goodbye.', True);
