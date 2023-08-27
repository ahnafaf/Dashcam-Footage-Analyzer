import os
from datetime import datetime
from datetime import timedelta
import fileSeperator

videoDateTimes = []
listofFiles = os.listdir('D:\dashcam\Front')
# List that contains [(Date, Ride No., FileName)]
finalList = []
# Returns a date object


# Adds object to list
def dateTimeAdder(files, target):
    for i in files:
        target.append(fileSeperator.dateObject(i))

# Takes a list of timestamps of dashcam videos and calculates number of rides
def countRides(dateObjects):
    rides = 1
    for i in range(1, len(dateObjects)):
        #print( dateObjects[i] - dateObjects[i-1])
        if dateObjects[i] - dateObjects[i-1] >= timedelta(minutes= 4):
            rides += 1
    return rides

dateTimeAdder(listofFiles, videoDateTimes)
print(countRides(videoDateTimes))