#import matplotlib.pyplot as plt
import csv
import os.path

def SaveCurrentValues(setTemp, currTemp, MY_FILE):	
	fields=[setTemp,currTemp]
	with open(MY_FILE, 'a+') as f:
    		writer = csv.writer(f)
    		writer.writerow(fields)

def updateGraph(setTemp, currTemp, MY_FILE):
	#First save the current values
	SaveCurrentValues(setTemp, currTemp, MY_FILE)
   



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
