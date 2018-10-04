#!/usr/bin/python

import subprocess
import time


# Contains the python script to run shell scripts
# Should try: to run script, if fails, return false


# If enable is true, turn on relay
# Returns time
def WTI_logic(enable, DIR, relayID):

    if enable:
        if enable_relay(DIR, relayID):
            return time.time()
        else:
            print("ERROR TURNING ON WTI SWITCH")

    elif not enable:
        if disable_relay(DIR, relayID)
            return time.time()
        else:
            print("ERROR TURNING OFF WTI SWITCH")


def enable_relay(DIR, relayID):
    # enable heating
    try:
        subprocess.call([DIR + "/Hardware_control/WTI_on.sh", str(relayID + 1)])

        time.sleep(1) #Wait because of telnet
        return True

    except:
        return False


def disable_relay(DIR, relayID):
    # disable relay
    try:
        subprocess.call(
            [DIR + "/Hardware_control/WTI_off.sh", str(relayID + 1)])  # Calls bash script to turn heating off

        time.sleep(1)  # Wait because of telnet
        return True

    except:
        return False
