import matplotlib.pyplot as plt
import csv

def SaveCurrentValues(setTemp, currTemp):

    >> > with open('eggs.csv', 'rb') as csvfile:
        ...
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    ...
    for row in spamreader:
        ...
        print ', '.join(row)


def updateGraph(setTemp, currTemp):
    myfile="/Users/Jord/Documents/PycharmProjects/RaspberryPiThermostat/data.csv"



    x=[]
    y=[]

    with open(myfile, 'r') as csvfile:
        plots= csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(row[0])
            y.append(row[1])


    plt.plot(x,y, marker='o')

    plt.title('Data from the CSV File: People and Expenses')

    plt.xlabel('Time')
    plt.ylabel('Temperature')

    plt.show()