#!/usr/bin/python

import subprocess
import time
import requests

# Contains the python script to run shell scripts
# Should try: to run script, if fails, return false


# If enable is true, turn on relay
# Returns actual physical state of relay
def Relay_logic(enable, relayID, DUMMY):

    if enable:

        if DUMMY:

            print("DUMMY TESTING: Relay was turned on")
            return True
        
        else: 

            enable_relay(relayID): #Enabling relay

            if check_state(relayID):
                print("Switch was turned ON")
                return True 

            else:
                print("ERROR: Switch is OFF")
                return False

    elif not enable:

        if DUMMY:

            print("DUMMY TEST: Relay was turned off")
            return False

        else: 

            disable_relay(relayID): #Disabling relay

            if check_state(relayID):
                print("ERROR: Switch is ON")
                return True

            else:
                print("Switch was turned OFF")
                return False


#Forcing all relays into starting state
def Relay_initialse(tank_list):

	print("Initially turn all relays off....\n")

    headers = {'X-CSRF': 'x',}
    data = {'value': 'true'}
    auth=('admin', '1234')

    response = requests.put('http://192.168.0.100/restapi/relay/outlets/all;/state/', headers=headers, data=data, auth=auth)

	# for relayID in tank_list:
	# 	disable_relay(DIR, relayID)
	
    print('\nRELAY initilisation complete\n****************************************')
		

def enable_relay(relayID):

    if relayID==None:
        return False

    relayID=relayID-1 #hack moving back to base zero for

    headers = {'X-CSRF': 'x',}  #not sure what this is
    data = {'value': 'true'}   #true for enable
    auth=('admin', '1234')

    # enable relay
    try:
        dummy = requests.put('http://192.168.0.100/restapi/relay/outlets/' + str(relayID) + '/state/', headers=headers, data=data, auth=auth)

    except:
        return False


def disable_relay(relayID):

    if relayID==None:
        return False
        

    relayID=relayID-1 #hack moving back to base zero for

    headers = {'X-CSRF': 'x',}  #not sure what this is
    data = {'value': 'false'}   #false for disable
    auth=('admin', '1234')
        
    # disable relay
    try:
        dummy = requests.put('http://192.168.0.100/restapi/relay/outlets/' + str(relayID) + '/state/', headers=headers, data=data, auth=auth)

    except:
        return False


def check_state(relayID)

    relayID=relayID-1 #hack moving back to base zero for

    headers = {'Accept': 'application/json',}
    auth=('admin', '1234')

    response = requests.get('https://192.168.0.100/restapi/relay/outlets/' + str(relayID) +'/state/', headers=headers, verify=False, auth=auth)

    return response

