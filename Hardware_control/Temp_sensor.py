#!/usr/bin/python

import os
import glob
import time
import pickle
import numpy as np

# Constants ############################################################################################################
########################################################################################################################
# Save path of current temperature
DIR = dir_path = os.path.dirname(os.path.realpath(__file__))
TEMPERATURE_FILE = DIR + '/SensorValues.txt'


def current_temp(Relay_ID):
	Relay_ID=Relay_ID-1 #moving base 1 to base 0
	currTemp = pickle.load(open(TEMPERATURE_FILE, 'r'))
	return currTemp[Relay_ID]

def get_device_file(sensorID):
	global BASE_DIR;
	file = None;
	try:
		file = BASE_DIR + sensorID + '/w1_slave';
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
		time.sleep(0.15);
		lines = read_temp_raw(device_file);
		equals_pos = lines[1].find('t=');
	temp_string = lines[1][equals_pos+2:];
	temp_c = float(temp_string)/1000.0;
	return (temp_c);

def get_average_temp(SENSOR_AVRG,device_file):
	AVERAGE_COUNT = SENSOR_AVRG
	
	total_c = 0
	for i in range(0,AVERAGE_COUNT):
		temp_c = read_temp(device_file)
		total_c += temp_c
	return total_c/AVERAGE_COUNT

def write_current(temp):
	global CURRENT_FILE
	
	

####MAIN CODE#########
def start_temp_readings(sensorID):
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-them')
	READ_DELAY = 0.1
	SENSOR_AVRG=3

	BASE_DIR = '/sys/bus/w1/devices'



	# First try to get the device file
	print('Finding sensor device file...\n');

	while(True):

			print("\n#######################################################")
			for index, sensor in enumerate(sensorID):

					device_file = get_device_file(sensor);

					avg_temp = -1;
					try:
							avg_temp = get_average_temp(SENSOR_AVRG, device_file);
					except KeyboardInterrupt:
							break;
					except Exception as e:
							print('Error getting temp reading from SENSOR ' + str(index)+': '+str(e));
							continue;


					print('\nCurrent Temp of SENSOR '+str(index+1) +', sensor ID: ' + sensor)
					print('({:d}) {:1.3f} C'.format(int(time.time()), avg_temp));
					sensorVAL[index]=avg_temp

			pickle.dump(sensorVAL, open(TEMPERATURE_FILE, 'w'))

			time.sleep(READ_DELAY);
