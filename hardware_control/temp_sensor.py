#!/usr/bin/python

import os
import time
import pickle
import numpy as np

# from .. import config

# CHANGE THIS
s1 = "28-000006dc6863"
s2 = "28-000006dc76f3"
s3 = "28-01131b65af91"
s4 = "28-02131694dcaa"
s5 = "28-01131e6b29e7"
s6 = "28-01131b9be090"
s7 = "28-0213139f02aa"
s8 = "28-01131bb70b6b"

# Sensor 1 for tank 1, is in the first place etc...
# s = config.sensor_ID
sensorID = [s1, s2, s3, s4, s5, s6, s7, s8]

# DONT CHANGE ANYTHING ELSE


READ_DELAY = 0.1
AVERAGE_COUNT = 3

BASE_DIR = '/sys/bus/w1/devices/'

# Save path of current temperature
DIR = dir_path = os.path.dirname(os.path.realpath(__file__))
CURRENT_FILE = DIR + '/SensorValues.txt'

DIR = dir_path = os.path.dirname(os.path.realpath(__file__))
CURRENT_FILE = os.path.join(DIR, '../data_logging/SensorValues.txt')
CURRENT_FILE = os.path.abspath(os.path.realpath(CURRENT_FILE))


def current_temp(Relay_ID):
    Relay_ID = Relay_ID - 1  # moving base 1 to base 0
    currTemp = pickle.load(open(CURRENT_FILE, 'r'))
    return currTemp[Relay_ID]


def get_device_file(sensorID):
    global BASE_DIR
    file = None
    try:
        file = BASE_DIR + sensorID + '/w1_slave'
    except:
        pass
    return file


def read_temp_raw(device_file):
    lines = None
    with open(device_file, 'r') as file:
        lines = file.readlines()
    return lines


def read_temp(device_file):
    lines = None
    equals_pos = -1
    while equals_pos < 0 or lines[0].strip()[-3:] != 'YES':
        time.sleep(0.15)
        lines = read_temp_raw(device_file)
        equals_pos = lines[1].find('t=')
    temp_string = lines[1][equals_pos + 2:]
    temp_c = float(temp_string) / 1000.0
    return (temp_c)


def get_average_temp(device_file):
    global AVERAGE_COUNT

    total_c = 0
    for i in range(0, AVERAGE_COUNT):
        temp_c = read_temp(device_file)
        total_c += temp_c
    return total_c / AVERAGE_COUNT


def write_current(temp):
    global CURRENT_FILE


# ###MAIN CODE#########
def main(sensorVAL, DUMMY):
    # First try to get the device file
    print('Starting Temp sensor...\n')

    #sensorVAL = np.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=np.float)
    #sensorVAL.fill(np.nan)

    if not DUMMY:

        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

    while (True):

        #print("\n#######################################################")

        if not DUMMY:

            for index, sensor in enumerate(sensorID):

                device_file = get_device_file(sensor)

                avg_temp = -1
                try:
                    avg_temp = get_average_temp(device_file)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    #print('Error getting temp reading from SENSOR ' + str(index) + ': ' + str(e))
                    continue;

                #print('\nCurrent Temp of SENSOR ' + str(index + 1) + ', sensor ID: ' + sensor)
                #print('({:d}) {:1.3f} C'.format(int(time.time()), avg_temp))
                sensorVAL[index] = avg_temp


        #conn.send(sensorVAL)
        #print("Sent the message: {}".format(sensorVAL))

        # pickle.dump(sensorVAL, open(CURRENT_FILE, 'w'))

        if DUMMY:
            for i in range(len(sensorVAL)):
                sensorVAL[i] = sensorVAL[i] + 1
            time.sleep(1)


        time.sleep(READ_DELAY)

    #conn.close()


####################################
if __name__ == "__main__":
    main()
