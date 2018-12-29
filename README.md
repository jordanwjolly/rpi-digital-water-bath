SUMMARY

This is a basic bang-bang temperature controller used for maintaining desired tempreatures in up to 8 seperate aquatic environments simultaneously.
It can be used to both heat, and cool an environment based off a desired temperature profile curve.

The system uses the following Hardware:

	- Network Power Switch from WTI
	- Raspberry Pi
	- <= 8 x Waterproof DS18B20 Digital temperature sensor for environmental sensing
	- <= 8 x Heating element
	- <= 8 x Cooling element

Where multiple water sources are required to be heated/cooled simatenously, a single cooler, heater, and tempreature sensor will be required per tank. 
A single setwork power switch is all thats required.

User options:

- A user can toggle a gui graph of temperature history turning on/off
- DUMMY flag allows testing on a regular PC with dummy data/values 
- All user settings for temperature curve control are edited in 'config.py'

GENERAL USER USE

Temperature sensors:
As the DS18B20 temperature sensor is a 1-wire device, as many of these sensors can all be connected to the same pull-up resistor circuirty
It is best if a user connects each of the sensors once at a time, and notes the unique sensor ID address.

User navigates to here:

cd /sys/bus/w1/devices/

Notes down the sensor ID, physically labels the sensor with a number 1-8, and then copies the sensor ID to the correspeonding slot in Temp_sensor.py


User specified temp:
User inputs the temprature_profile.py script


TO GET SOFTWARE RUNNING
WTI NETWORK POWER SWITCH
This device is super old, and the standby power battery has stopped working. If the unit is turned off, It is therefore neccesary to redo the networking settings.

Open a serial terminal (recommend using Arduino IDE Serial Monitor) to USB0, with newline and carrige return used.
Press 'Enter' key to see options
Type '/N' to get to network settings.
type '1' and set the ip address to 192.168.168.168 
type '2' and set netmask to 255.255.255.0
Type '/G' to get to general settings
Type '6' and turn 'command echo' to the off state
'/X' to exit. The device should now be able to be pinged from your pi

STARTING THE PROGRAM
Open up a terminal on the raspberry pi.

change directories "cd /RPiAquariumTempController"

type "./launch.sh"

...sit back, relax, and watch those temperature controlled aquariums look after your aqautic animals in style
