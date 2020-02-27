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




def animate(frame):
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
        print(maxStart, maxSpan)

        data = np.clip(data, float('-inf'), 0)
        ax1.plot(theta,data)
ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()

