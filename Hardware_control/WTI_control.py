#!/usr/bin/python

import subprocess
import time
import requests

# Contains the python script to run shell scripts
# Should try: to run script, if fails, return false


# If enable is true, turn on relay
# Returns time
def WTI_logic(enable, DIR, relayID, DUMMY):
    if enable:
        if DUMMY:
            print("DUMMY TEST: WTI SWITCH TURNED ONNNNN")
        elif enable_relay(DIR, relayID):
            print("WTI SWITCH TURNED ON")
        else:
            print("ERROR TURNING ON WTI SWITCH")

    elif not enable:
        if DUMMY:
            print("DUMMY TEST: WTI SWITCH TURNED OFFFFF")
        elif disable_relay(DIR, relayID):
            print("WTI SWITCH TURNED OFF")
        else:
            print("ERROR TURNING OFF WTI SWITCH")

#Forcing all relays into starting state
def WTI_initialse(tank_list, DIR):
	print("Initially turn all relays off....\n")
	for relayID in tank_list:
		disable_relay(DIR, relayID)
	print('\nRELAY initilisation complete\n****************************************')
		

def enable_relay(DIR, relayID):
	    
    if relayID==None:
    	return False
    	
    # enable heating
    try:
        subprocess.Popen([DIR + "/Hardware_control/WTI_on.sh", str(relayID)])

        time.sleep(2) #Wait because of telnet. Is needed for the case where telenet is being used 
        return True

    except:
        return False


def disable_relay(DIR, relayID):
    
    if relayID==None:
    	return False
    	
    # disable relay
    try:
        subprocess.Popen([DIR + "/Hardware_control/WTI_off.sh", str(relayID)])  # Calls bash script to turn heating off

        time.sleep(2)  # Wait because of telnet
        return True

    except:
        return False
