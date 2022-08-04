import csv
import time
from datetime import datetime
import pandas as pd

def lineIsSuccess(line):
    depatureTime = datetime.strptime(line[2].strip(), "%H:%M")
    arrivalTime = datetime.strptime(line[1].strip(), "%H:%M")
    delta = depatureTime-arrivalTime
    return delta.total_seconds()  >= (180*60)

def getSortedArrayFromCsv(filename):
    try:
        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            lines = []
            for row in datareader:
                row[3] = ""
                lines.append(row)
            data = sorted(lines, key = lambda row: datetime.strptime(row[1].strip(), "%H:%M"))
            return data
    except Exception as e:
        print("Exception, the file was not changed")
        return []

def getFlightInfoFromFlightNumber(filghtNumber):
    with open('flights.csv', 'r') as csvfile:
        datareader = csv.reader(csvfile)
        lines = []
        for row in datareader:
            if row[0]==filghtNumber:
                return row
        return None

def updateFlightInCsvAndReturnIfChanged(flightNumber, arrivalTime, depatureTime, success):
    updatedRow = [flightNumber, arrivalTime, depatureTime, str(success)]
    newFileRows = []
    rowChanged = False
    file = open("flights.csv", "r")
    lines = csv.reader(file)
    for line in lines:
        if(line[0]==flightNumber):
            newFileRows.append(updatedRow)
            rowChanged = True

        else:
            newFileRows.append(line)

    file.close()
    file = open("flights.csv", "w", newline='')
    data = csv.writer(file)
    data.writerows(newFileRows)  
    file.close()
    return rowChanged
    


def main():
    filename = 'flights.csv'
    sortedArray = getSortedArrayFromCsv(filename)
    numberOfSuccesses = 0
    for row in sortedArray:
        if lineIsSuccess(row) and numberOfSuccesses<20:
            row[3] = 'success'
            numberOfSuccesses+=1
        else:
            row[3] = 'fail'
    try: 
        f = open('flights.csv', 'w', newline='')
        writer = csv.writer(f)
        for row in sortedArray:
            writer.writerow(row)
        f.close()
    except Exception as e:
        print("Exception, the file was not changed")
    
if __name__ == "__main__":
    main()