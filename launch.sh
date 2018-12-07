#!/bin/bash

(cd Hardware_control/ && xterm -e python Temp_sensor_OLD.py&)

sleep 10

xterm -e python temperature_profile.py&
