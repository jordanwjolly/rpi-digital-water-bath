#import matplotlib.pyplot as plt
import csv, time
import os.path
import matplotlib.pyplot as plt


# saves the current RelayID, temps, and time in one .csv per tank
def saveCurrentValue(Set_Temp, Current_Temp, Relay_ID, GRAPH_DIR):

	GRAPH_NAME = "Tank_" + str(Relay_ID)
	GRAPH_FILE = GRAPH_DIR + GRAPH_NAME + ".csv"

	fields = [Relay_ID]
	fields.extend([time.time()])
	fields.extend([Set_Temp])
	fields.extend([Current_Temp])
	#print(fields)
	with open(GRAPH_FILE, 'a+') as f:
		writer = csv.writer(f)
		writer.writerow(fields)

def updateGraph(GRAPH_DIR, Relay_ID):

	GRAPH_NAME = "Tank_" + str(Relay_ID)
	GRAPH_FILE = GRAPH_DIR + GRAPH_NAME + ".csv"
	
	t = []
	set_temp = []
	curr_temp = []

	with open(GRAPH_FILE,'r') as csvfile:
		plots = csv.reader(csvfile, delimiter=',')
		for row in plots:
			t.append((row[1]))
			set_temp.append(row[2])
			curr_temp.append(row[3])

	plt.plot(t,set_temp, 'bo')
	plt.plot(t,curr_temp, 'go')
	plt.xlabel('time')
	plt.ylabel('current temp')
	plt.title(GRAPH_NAME)
	plt.legend()
	plt.show()
	plt.pause(0.001)


	# plt.ion()
	# plt.show()
    #
	# t = []
	# set_temp = []
	# curr_temp = []
    #
	# with open(GRAPH_FILE, 'r') as csvfile:
	# 	plots = csv.reader(csvfile, delimiter=',')
	# 	for row in plots:
	# 		t.append((row[1]))
	# 		set_temp.append(row[2])
	# 		curr_temp.append(row[3])
	# # plt.ion()
	# plt.hold(True)
	# plt.plot(t, set_temp, 'bo')
	# plt.plot(t, curr_temp, 'go')
	# plt.xlabel('time')
	# plt.ylabel('current temp')
	# plt.title('Interesting Graph\nCheck it out')
	# plt.legend()
	# plt.draw()
	# plt.pause(0.001)
	
	
   



 #myfile="/Users/Jord/Documents/PycharmProjects/RaspberryPiThermostat/data.csv"



	#x=[]
	#y=[]

	#with open(myfile, 'r') as csvfile:
	 #   plots= csv.reader(csvfile, delimiter=',')
	 #   for row in plots:
	  #      x.append(row[0])
	   #     y.append(row[1])


	#plt.plot(x,y, marker='o')

	#plt.title('Data from the CSV File: People and Expenses')

	#plt.xlabel('Time')
	#plt.ylabel('Temperature')

	#plt.show()
