#import matplotlib.pyplot as plt
import csv, time
import os.path
import matplotlib.pyplot as plt


# saves the current RelayID, temps, and time in one .csv per tank
def saveCurrentValue(t, Set_Temp, Current_Temp, Relay_ID, GRAPH_DIR):

	GRAPH_NAME = "Tank_" + str(Relay_ID)
	GRAPH_FILE = GRAPH_DIR + GRAPH_NAME + ".csv"

	fields = [Relay_ID]
	fields.extend([int(t)])
	fields.extend([int(Set_Temp)])
	fields.extend([int(Current_Temp)])
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
