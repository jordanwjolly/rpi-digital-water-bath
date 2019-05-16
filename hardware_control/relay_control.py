#!/usr/bin/python

#import requests
import time


# If enable is true, turn on relay
# Returns actual physical state of relay
def relayPrintState(enable, relayID):
    print(
        "---------Relay " + str(relayID) + ": was turned " +
        str(enable) + "----------------------")


def relayLogic(enable, relayID, DUMMY):

    if enable:

        if DUMMY:
            relayPrintState(enable, relayID)

        else:
            enableRelay(relayID)
            time.sleep(1)
            # Checking hardware to validate caommand
            if True: #checkState(relayID):
                relayPrintState(enable, relayID)

            else:  # Failed to turn on relay

                enable = not enable
                print("ERROR")
                relayPrintState(enable, relayID)

    elif not enable:

        if DUMMY:

            relayPrintState(enable, relayID)

        else:

            disableRelay(relayID)  # Disabling relay
            time.sleep(1)

            if False: #checkState(relayID):

                enable = not enable
                print("ERROR")
                relayPrintState(enable, relayID)

            else:
                relayPrintState(enable, relayID)

    return enable


# Forcing all relays into starting state
def RelayInitialse(tank_list):

    print("Initially turn all relays off....\n")
    for relayID in tank_list:
	    disableRelay(relayID)

    print('\nRELAY initilisation complete\n****************************************')


def enableRelay(relayID):

    if relayID is None:
        return False

    # enable relay
    try:
        print('')
        #r = requests.get('http://192.168.0.100/outlet?'+str(relayID) + '=ON',  auth=('admin', '1234'))
    except:
        return False


def disableRelay(relayID):

    if relayID is None:
        return False

    # disable relay
    try:
        print('')
        #r = requests.get('http://192.168.0.100/outlet?'+str(relayID) + '=OFF',  auth=('admin', '1234'))

    except:
        return False


def checkState(relayID):

    relayID = relayID - 1  # hack moving back to base zero for

    headers = {'Accept': 'application/json', }
    auth = ('admin', '1234')
    print('')
    #response = requests.get(
     #   'https://192.168.0.100/restapi/relay/outlets/' +
    #    str(relayID) + '/state/', headers=headers, verify=False, auth=auth)

    return response
