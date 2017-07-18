import os
import sys
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt


x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
y = [1,3,2,5,7,5,7,6,5,8,5,6,2,3,6,7,8,3,4,2,0]


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

###Actual Data###

x6 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]
y6 = [83.84178066,87.39763475,64.64365325,40.01920089,85.80916849,299.8705668,
367.928902,627.3694875,660.1910653,799.1058133,869.9513472,697.7303056,
637.8174963,788.3672113,495.7691243,665.6148409,243.2329956,252.2589057,
244.333821,429.9616539,427.2951582,496.1439951,400.3583115,534.9038794,
464.5044923,786.5638874,670.2328772,721.3013296,683.4684898,695.3791659,
489.5308738,228.2087025,47.74828691,58.90253631]
y6_array = np.array(y6)
y6_norm = (y6_array-min(y6_array))/(max(y6_array)-min(y6_array))



x7 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
y7 = [53.96109247,51.94557391,114.7658106,27.06396354,99.93580126,194.7453239,
      235.6069186,128.3276648,85.55980883,281.4654769,266.8634226,340.3770385,
      626.6450547,469.4743098,401.5017353,516.1209706,602.3136578,530.3262038,
      446.591563,64.5703435,622.618999,283.5170534,105.1207242,146.1335966]
y7_array = np.array(y7)
y7_norm = (y7_array-min(y7_array))/(max(y7_array)-min(y7_array))



x8 = [0,1,2,3,4,5,6,7,8,9]
y8 = [41.86923186,157.9233306,78.32229816,114.7636794,63.13983779,333.8135138,
      294.7568036,547.4530457,58.80570078,95.33139207]
y8_array = np.array(y8)
y8_norm = (y8_array-min(y8_array))/(max(y8_array)-min(y8_array))


x9 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
y9 = [27.55783072,190.6430918,104.6789475,127.6743658,39.62365388,334.1366975,
      532.374108,543.1851096,734.3471338,673.79914,756.4371357,505.7226297,
      467.4672948,776.506598,728.0397807,338.4085565,144.4747328,305.952343,
      439.3434027,424.0859447,483.4180654,481.107404,218.0562739,213.8509214,
      321.8840737,67.83357248,107.5709577]
y9_array = np.array(y9)
y9_norm = (y9_array-min(y9_array))/(max(y9_array)-min(y9_array))


x10 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
y10 = [79.78049987,22.35571616,86.65252653,107.1472917,168.3670755,306.0597022,
       365.5976883,638.2290282,711.5170091,363.02013,691.4936899,403.2916098,
       397.9510363,483.553652,448.342882,441.3851953,585.8438515,330.2484436,
       418.7523215,93.84705845,86.968796,248.0338541,309.5514714,72.89888678,
       109.9545831]
y10_array = np.array(y10)
y10_norm = (y10_array-min(y10_array))/(max(y10_array)-min(y10_array))



x11 = [0,1,2,3,4,5,6,7]
y11 = [141.1769328,74.28460733,69.87869383,93.24833446,157.2035798,314.72753,
       111.3037572,138.3456861]
y11_array = np.array(y11)
y11_norm = (y11_array-min(y11_array))/(max(y11_array)-min(y11_array))



x12 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
y12 = [110.8419061,231.1090287,224.9493691,78.3870788,83.49706925,409.1805718,
       522.9315153,472.6651092,141.9126826,288.720796,366.1343076,54.32835323,
       321.7592054,134.254153,103.8176461]
y12_array = np.array(y12)
y12_norm = (y12_array-min(y12_array))/(max(y12_array)-min(y12_array))



x = x12
y = y12_norm


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

                print log_input,np.log10((1+log_input))

                hold = mean1 + sign*(np.absolute(np.log10((1+5*log_input))))
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