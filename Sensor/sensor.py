#!/usr/bin/python

import os;
import glob;
import time;
import json;

os.system('modprobe w1-gpio');
os.system('modprobe w1-therm');

READ_DELAY = 0.5;
AVERAGE_COUNT = 3;

BASE_DIR = '/sys/bus/w1/devices/';

CURRENT_FILE = '/home/pi/thermostat/current.json';

def get_device_file():
	global BASE_DIR;
	file = None;
	try:
		file = glob.glob(BASE_DIR + '28*')[0] + '/w1_slave';
	except:
		pass;
	return file;

def read_temp_raw(device_file):
	lines = None;
	with open(device_file, 'r') as file:
		lines = file.readlines();
	return lines;

def read_temp(device_file):
	lines = None;
	equals_pos = -1;
	while equals_pos < 0 or lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2);
		lines = read_temp_raw(device_file);
		equals_pos = lines[1].find('t=');
	temp_string = lines[1][equals_pos+2:];
	temp_c = float(temp_string)/1000.0;
	temp_f = temp_c * 9.0 / 5.0 + 32.0;
	return (temp_c, temp_f);

def get_average_temp(device_file):
	global AVERAGE_COUNT;
	
	total_f = 0;
	for i in range(0,AVERAGE_COUNT):
		temp_c, temp_f = read_temp(device_file);
		total_f += temp_f;
	return total_f/AVERAGE_COUNT;

def write_current(temp):
	global CURRENT_FILE;	

	s = json.dumps({"temperature":temp, 'date':int(time.time())});
	with open(CURRENT_FILE, 'w') as file:
		file.write(s);

# First try to get the device file

print('Finding sensor device file...\n');

device_file = None;
while (device_file is None):
	print('Not found');
	device_file = get_device_file();
	time.sleep(0.5);

print('\nDevice found!\n');

# Now the actual sensor loop
while (True):
	avg_temp = -1;
	try:
		avg_temp = get_average_temp(device_file);
	except KeyboardInterrupt:
		break;
	except Exception as e:
		print('Error getting temp reading: '+str(e));
		continue;
	
	if(avg_temp < 0):
		continue;
	
	write_current(avg_temp);
	print('({:d}) {:1.3f} F'.format(int(time.time()), avg_temp));
	time.sleep(READ_DELAY);
