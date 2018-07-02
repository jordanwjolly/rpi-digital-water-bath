#!/usr/bin/python

# Imports ##############################################################################################################
########################################################################################################################

import os;			# OS functions
import json;			# JSON library
import time;			# Time functions
import subprocess

# FILE PATH INFO
DIR = dir_path = os.path.dirname(os.path.realpath(__file__))
CURRENT_TEMP_FILE = DIR+'/current.json'
SENSOR_SCRIPT_FILE = DIR + '/Hardware_control/Temp_sensor.py'
GRAPH_FILE = DIR + '/Software_control/Graph_values.csv'

while (1):
    subprocess.call(DIR+"/Hardware_control/WTI_off.sh")
    subprocess.call(DIR+"/Hardware_control/WTI_on.sh")
