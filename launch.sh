#!/bin/bash

(cd hardware_control/ && xterm -e python temp_sensor.py&)

sleep 10

xterm -e python main.py&
