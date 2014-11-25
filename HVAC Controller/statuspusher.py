#!/usr/bin/python

######################################################################################################
# StatusPusher.py
# Pushes the values from status.json up to the website.
######################################################################################################

# Imports ############################################################################################

import sys;
import time;
import json;
import requests;

# Constants ##########################################################################################

DIR = '/home/pi/thermostat';
STATUS_FILE = DIR+'/status.json';
PAUSE_INTERVAL = 2;
UPDATE_URL = "https://XXXXX/rpi/update_status.php"; # Replace with your remote URL
VERBOSE = True;

CONTROLLER_ID = "XXXXX"; # Change this to your public controller ID.
CONTROLLER_KEY = "xxxxxxxxxxxxxxxxxxxxxx"; # Change this to your private controller key. 

# Variables ##########################################################################################

# Functions ##########################################################################################

def getStatus():
	global STATUS_FILE;
        s = None;
        with open(STATUS_FILE) as file:
                s = file.read();
        data = json.loads(s);
        return data;

def sendUpdate(data):
	global UPDATE_URL;
	global CONTROLLER_ID;
	global CONTROLLER_KEY;
	
	payload = {
		'id':		CONTROLLER_ID,
		'key':		CONTROLLER_KEY,
		'data':		json.dumps(data)
	};
	try:
		r = requests.post(UPDATE_URL, data=payload);
		response = json.loads(r.text);
		print('R: '+(r.text));
		if(response["success"] is True):
			return True;
	except Exception, e:
		print('Exception: '+str(e));
		return False;

def writeVerbose(str, newline = False):
	global VERBOSE;
	if(not VERBOSE):
		return;
	print(str);
	if(newline):
		print(' ');

# Main ###############################################################################################

writeVerbose('Beginning status pusher script.');
writeVerbose('Press Ctrl+C to stop loop.', True);

while(True):
	try:
		data = getStatus();
	except:
		writeVerbose('Could not fetch current status data.');
		time.sleep(1);
		continue;
	writeVerbose('Updating status...');
	if(sendUpdate(data)):
		writeVerbose('Update successful!');
	else:
		writeVerbose('Update failed.');
	writeVerbose(' ');
	time.sleep(PAUSE_INTERVAL);

writeVerbose(' ');
writeVerbose('Status pusher closing, goodbye.', True);
