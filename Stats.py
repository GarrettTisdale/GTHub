import os
import re
import sys
import csv
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt


csv1 = open('Data_Matrix_csv_test_frames.csv', 'rb')
csv2 = open('Data_Matrix_csv_test_intensity.csv', 'rb')


d_list = {}
d_intensity = {}
d_stitched = {}
d_name = {}
len_row1 = 0
len_row2 = 0
row_num1 = 0
row_num2 = 0
row_num3 = 0
max_index = 0


for row in csv1:
    if row_num1 == 0:
        len_row1 = len(row)
        burst_number_save = 1
        row_list = row.split(',')
        name_burst_number_save = 1

        for i in row_list:
            d_name["Burst{0}".format(name_burst_number_save)] = re.findall("\d+[\.]?", i)

            
            a = d_name["Burst"+str(name_burst_number_save)]
            
            #print a[1]
            
            name_burst_number_save += 1
        row_num1 = 1
    max_index = d_name["Burst"+str(name_burst_number_save-1)][0]
    break


for row in csv1:
    len_row1 = len(row)
    burst_number_save = 1
    row_list = row.split(',')
    
    for i in range(0,len(row_list)):
        if "Burst{0}".format(burst_number_save) not in  d_list:
            d_list["Burst{0}".format(burst_number_save)] = [row_list[i].rstrip()]
            burst_number_save += 1
            
        if "Burst{0}".format(burst_number_save) in  d_list:

            a = d_list["Burst{0}".format(burst_number_save)]                
            a.append(row_list[i].rstrip())
            burst_number_save += 1
                
        
hold = []
for key in d_list:
    a = d_list[key]
    for i in a:
        if i:
            hold.append(i)
    d_list[key] = hold
    hold = []

for row in csv2:
    if row_num3 != 0:
        len_row2 = len(row)
        burst_number_save = 1
        row_list = row.split(',')
        
        for i in range(0,len(row_list)):
            if "Burst{0}".format(burst_number_save) not in  d_intensity:
                d_intensity["Burst{0}".format(burst_number_save)] = [row_list[i].rstrip()]
                burst_number_save += 1
                
            if "Burst{0}".format(burst_number_save) in  d_intensity:
                a = d_intensity["Burst{0}".format(burst_number_save)]                
                a.append(row_list[i].rstrip())
                burst_number_save += 1
    row_num3 = 1

        
hold = []
for key in d_intensity:
    a = d_intensity[key]
    for i in a:
        if i:
            hold.append(i)
    d_intensity[key] = hold
    hold = []


for i in range(1,len(d_name)+1):
    for x in range(1, int(max_index)):
        if int(d_name["Burst"+str(i)][0]) == x:
            if "Burstx{0}".format(str(x)) not in  d_stitched:
                d_stitched["Burstx{0}".format(x)] = []
                a = d_stitched["Burstx"+str(x)]
                for z in d_list["Burst"+str(i)]:
                    a.append(z)
                    
                d_stitched["Bursty{0}".format(x)] = []
                b = d_stitched["Bursty"+str(x)]
                for z in d_intensity["Burst"+str(i)]:
                    b.append(z)
                
            if "Burstx{0}".format(str(x)) in  d_stitched:
                a = d_stitched["Burstx{0}".format(x)]  
                for z in d_list["Burst"+str(i)]:
                    a.append(z)
                    
                b = d_stitched["Bursty{0}".format(x)]  
                for z in d_intensity["Burst"+str(i)]:
                    b.append(z)
             
print d_stitched["Burstx2"]
print d_stitched["Bursty2"]

print len(d_stitched["Burstx2"]), len(d_stitched["Bursty2"])             
             



    
fig, ax = plt.subplots()
ax.plot(d_stitched["Burstx2"], d_stitched["Bursty2"], 'b-')
ax.set_xlabel('Frame')
ax.set_ylabel('Intensity', color='b')
ax.tick_params('y', colors='b')
    
plt.show()
plt.clf()
plt.close()




