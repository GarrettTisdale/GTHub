import os
import sys
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt


x = [0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,0,0,0,0]
y = [0,0,0,0,0,1,3,2,5,7,5,7,6,5,8,5,6,2,3,6,7,8,3,4,2,0,0,0,0,]


x1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
y1 = [3,1.5,2,1.25,1.65,2.75,2.15,2.75,3.75,3,4,1.85,4,3,3.75,2.15,1.35,1.75,1.25]


x2 = [0,1,2,3,4,5,6,7,8,9,10,11,12]
y2 = [1,2.5,.65,3,1.75,4,3,3.85,1,3.85,3.5,4,1]


x3 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
y3 = [1,1.65,1.15,3,2,4.15,3.75,5,4.65,5,4,4.15,3.15,2,3.15,1.25]


x4 = [0,1,2,3,4,5,6,7,8,9,10,11,12]
y4 = [1,1.25,.65,1.35,1.2,3.4,4.5,2.8,1,.65,1.12,1.2,.65]


x5 = [0,1,2,3,4,5,6,7,8,9,10,11,12]
y5 = [1,1.25,1.1,1.35,1.2,1.5,4.5,1.5,1,1.25,1.12,1.2,.65]


x = x1
y = y1


fig, ax1 = plt.subplots()

ax1.plot(x, y, 'b-')
ax1.set_xlabel('Frame')
ax1.set_ylabel('Intensity', color='b')
ax1.tick_params('y', colors='b')

plt.show(block=False)



len_x = len(x)


normal_bin_smoothing = []
for i in range(0,len(x)-2):
    hold = np.mean([y[i], y[i+1],y[i+2]])
    normal_bin_smoothing.append(hold)



fig, ax1 = plt.subplots()

ax1.plot(range(0,len(normal_bin_smoothing)), normal_bin_smoothing, 'b-')
ax1.set_xlabel('Frame')
ax1.set_ylabel('Intensity', color='b')
ax1.tick_params('y', colors='b')

plt.show(block=False)



count_num = 0

mean_bin_smoothing = []
for i in range(0,len(x)):
    if x[0] == x[i]:
        hold = np.mean([y[i], y[i+1],y[i+2]])
        print y[i],y[i+1], y[i+2]
        mean_bin_smoothing.append(hold)

    if x[-3] == x[i]:
        hold = np.mean([y[i], y[i+1],y[i+2]])
        mean_bin_smoothing.append(hold)
        break

    if x[0] != x[i]:
        if x[-3] != x[i]:
            mean1 = np.mean([y[i], y[i + 1], y[i + 2]])
            mean2 = np.mean([y[i-1], y[i+3]])

            if np.absolute(mean1-mean2) > 0:
                log_input = float((mean1 - mean2))

                if log_input >= 0:
                    sign = 1
                else:
                    sign = -1

                log_input = np.absolute(log_input)

                print log_input

                hold = mean1 + sign*(1.25*np.log10(10*log_input))
                mean_bin_smoothing.append(hold)


            else:
                hold = mean1
                mean_bin_smoothing.append(hold)

fig, ax1 = plt.subplots()

ax1.plot(range(0,len(mean_bin_smoothing)), mean_bin_smoothing, 'b-')
ax1.set_xlabel('Frame')
ax1.set_ylabel('Intensity', color='b')
ax1.tick_params('y', colors='b')

plt.show(block=False)






normal_bin_smoothing2 = []

x = range(0,len(mean_bin_smoothing))
y = mean_bin_smoothing

normal_bin_smoothing2.append(normal_bin_smoothing[0])

for i in range(0,len(x)-2):
    hold = np.mean([y[i], y[i+1],y[i+2]])
    normal_bin_smoothing2.append(hold)

normal_bin_smoothing2.append(normal_bin_smoothing[-1])


fig, ax1 = plt.subplots()

ax1.plot(range(0,len(normal_bin_smoothing2)), normal_bin_smoothing2, 'b-')
ax1.set_xlabel('Frame')
ax1.set_ylabel('Intensity', color='b')
ax1.tick_params('y', colors='b')

plt.show(block=True)

