THIS PROJECT WAS IMPLEMENTED TO SUPPORT THE RESEARCH FOUND IN THE PAPER BELOW


Loughland I., Lau G.Y., Jolly J., and Seebacher F. (2019) The effect of the rate of thermal change on mitochondrial ROS production and subsequent oxidative damage.


SUMMARY


This is a basic bang-bang temperature controller used for maintaining desired temperatures in up to 8 seperate aquatic environments simultaneously.
It can be used to both heat, and cool an environment based off a desired temperature profile curve.

The system uses the following Hardware:

	- Data-center PDU from Data-loggers.com. Model: 222
	- Raspberry Pi
	- <= 8 x Waterproof DS18B20 Digital temperature sensor for environmental sensing
	- <= 8 x Heating element
	- <= 8 x Cooling element

Where multiple water sources are required to be heated/cooled simatenously, a single cooler, heater, and tempreature sensor will be required per tank. A single network power switch is all thats required.

USER OPTIONS:

	- A flag "DUMMY" allows testing on a regular PC with dummy data/values 
	- User settings for temperature curve control are edited in 'config.py'
		- Number of Tanks used
		- Desired Temperature curve
		- Run time
		- Refresh rate of Controller (per tank)
	- A variable "HEATER_RECOVERY_TIME" can be set to correct for the lag in heater element cooling

GENERAL USE:

Temperature sensors:
As the DS18B20 temperature sensor is a 1-wire device, as many of these sensors can all be connected to the same pull-up resistor circuirty.

During setup, It is best if a user connects each of the sensors once at a time, and notes the unique sensor ID address.

User navigates to here:

	cd /sys/bus/w1/devices/

Notes down the sensor ID, physically labels the sensor with a number 1-8, and then copies the sensor ID to the correspeonding slot in Temp_sensor.py


STARTING THE PROGRAM

Open up a terminal on the raspberry pi.

	change directories "cd /RPiTempController"

	type "python launch.py"
	
DONE
