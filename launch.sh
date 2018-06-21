#!/bin/bash

stat -c %Y current.json | sed 's/current.json//'
python Hardware_control/Temp_sensor.py & 

python temperature_profile.py
