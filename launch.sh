#!/bin/bash

(cd hardware_control/ && xterm -e python temp_sensor.py&)

sleep 15

xterm -e python main.py&
