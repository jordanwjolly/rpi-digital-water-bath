#import matplotlib.pyplot as plt
import csv, time
import os.path
import matplotlib.pyplot as plt


def SaveCurrentValues(setTemps, currTemps, MY_FILE):	
	fields=[time.time()]
	fields.extend(setTemps)
	fields.extend(currTemps)
	#fields.extend(heatingOn)
	print(fields)
	with open(MY_FILE, 'a+') as f:
    		writer = csv.writer(f)
    		writer.writerow(fields)

def updateGraph(setTemp, currTemp, MY_FILE):
	plt.ion()
	plt.show()
	#First save the current values
	SaveCurrentValues(setTemp, currTemp, MY_FILE)
	
	t = []
	set_temp = []
	curr_temp = []

	with open(MY_FILE,'r') as csvfile:
		plots = csv.reader(csvfile, delimiter=',')
		for row in plots:
			t.append((row[0]))
			set_temp.append(row[1])
			curr_temp.append(row[2])
	#plt.ion()
	plt.hold(True)
	plt.plot(t,set_temp, 'bo')
	plt.plot(t,curr_temp, 'go')
	plt.xlabel('time')
	plt.ylabel('current temp')
	plt.title('Interesting Graph\nCheck it out')
	plt.legend()
	plt.draw()
	plt.pause(0.001)
	
	
   



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
