#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyurg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import time


# For initializing.
urg = pyurg.UrgDevice()

# Connect to the URG device.
# If could not conncet it, get False from urg.connect()
if not urg.connect():
    print 'Could not connect.'
    exit()

# Get length datas and timestamp.
# If missed, get [] and -1 from urg.capture()
urg.laser_on()

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1, polar=True)

time.sleep(2)

print 'Calibrating Room...'
data, timestamp = urg.capture()
streamLen = len(data)
avg = np.zeros(streamLen)
calibSteps = 10
for t in range(calibSteps):
    data, timestamp = urg.capture()
    data = np.asarray(data)
    avg += data
avg /= calibSteps
print 'Room Calibrated.'


def inRange(start, span, range):
    mid   = range[0]
    width = range[1]

    peak = start + span/2

    return (peak > mid - width) and (peak < mid + width)


def write_to_file(val):
    dataFile = open("../websocket/data.txt",'a')
    dataFile.write(val)
    dataFile.close()



entrance = []
exit = []
inEntrance = False
inExit = False
while True:

    data, timestamp = urg.capture()

    if(np.sum(data) > 1):
        ang = 2*3.14 * (270.0/360)
        theta = np.linspace(0,ang,num=streamLen)
        ax1.clear()
        data -= avg

        maxSpan = 0
        maxStart = 0
        span  = 0
        start = 0

        for i in range(streamLen):
            if(data[i] < -1):
                span += 1
            else:
                if(span > maxSpan):
                    maxSpan  = span
                    maxStart = start
                span = 0
                start = i
        #print(maxStart, maxSpan)

        entranceRange   = [480,40]
        entranceFallout = [480,60]
        exitRange   = [400,40]
        exitFallout = [400,60]

        midP = maxStart + maxSpan/2
        if(maxSpan > 15 and midP > 350 and midP < 500):
            print(midP)
        
            if inRange(maxStart, maxSpan, entranceRange) and not inEntrance:
                entrance.append(timestamp)
                print("inEntrance")
                inEntrance = True

            elif not inRange(maxStart, maxSpan, entranceFallout):
                inEntrance = False

            if inRange(maxStart, maxSpan, exitRange) and not inExit:
                exit.append(timestamp)
                print("inExit")
                inExit = True

            elif not inRange(maxStart, maxSpan, exitFallout):
                inExit = False



            if(len(entrance) > 0) and (len(exit) > 0):
                e0 = entrance.pop(0)
                e1 = exit.pop(0)
                

                if(e0 < e1):
                    write_to_file(":[0," + str(timestamp) + "]")
                else:
                    write_to_file(":[1," + str(timestamp) + "]")

        else:
            inEntrance = False
            inExit = False
            entrance = []
            exit = []






