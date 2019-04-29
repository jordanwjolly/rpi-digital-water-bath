#!/usr/bin/python

import subprocess
import time
import requests

# Contains the python script to run shell scripts
# Should try: to run script, if fails, return false


# If enable is true, turn on relay
# Returns actual physical state of relay
def relayPrintState(enable, relayID):
    print("---------Relay "+ str(relayID)+ ": was turned "+ str(enable)+ "----------------------")


def relayLogic(enable, relayID, DUMMY):

    if enable:

        if DUMMY:
            relayPrintState(enable, relayID)
        
        else: 

            enableRelay(relayID) #Enabling relay

            if checkState(relayID): #checking if relay state is on
                relayPrintState(enable, relayID)

            else: #Failed to turn on relay
                
                enable = not enable
                print("ERROR")
                relayPrintState(enable, relayID)

    elif not enable:

        if DUMMY:

            relayPrintState(enable, relayID)

        else: 

            disableRelay(relayID) #Disabling relay

            if checkState(relayID):
                
                enable = not enable
                print("ERROR")
                relayPrintState(enable, relayID)

            else:
                relayPrintState(enable, relayID)

    return enable


#Forcing all relays into starting state
def RelayInitialse(tank_list):

    print("Initially turn all relays off....\n")
    headers = {'X-CSRF': 'x',}
    data = {'value': 'true'}
    auth=('admin', '1234')

    response = requests.put('http://192.168.0.100/restapi/relay/outlets/all;/state/', headers=headers, data=data, auth=auth)

	# for relayID in tank_list:
	# 	disableRelay(DIR, relayID)
	
    print('\nRELAY initilisation complete\n****************************************')
		

def enableRelay(relayID):

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


def disableRelay(relayID):

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


def checkState(relayID):

    relayID=relayID-1 #hack moving back to base zero for

    headers = {'Accept': 'application/json',}
    auth=('admin', '1234')

    response = requests.get('https://192.168.0.100/restapi/relay/outlets/' + str(relayID) +'/state/', headers=headers, verify=False, auth=auth)

    return response

