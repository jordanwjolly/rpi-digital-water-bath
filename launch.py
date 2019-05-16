#!/usr/bin/python


import multiprocessing
from hardware_control import temp_sensor
import control
import config



# Main
def main():

    INITIALISE = config.initialisation_variables()

    # Starting multiprocess for temp sensor shared memory
    current_temp = multiprocessing.Array('d', [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    p1 = multiprocessing.Process(target=temp_sensor.main, args=(current_temp, INITIALISE.DUMMY))

    # starting main controller process
    p2 = multiprocessing.Process(target=control.main, args=(current_temp,))

    # running processes
    p1.start()
    p2.start()

    # wait until processes finish
    p1.join()
    p2.join()


####################################
if __name__ == "__main__":
    main()