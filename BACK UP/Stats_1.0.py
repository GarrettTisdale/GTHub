import os
import re
import sys
import csv
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


series = 100

csv1 = open('Test_Matrix_csv_test_frames.csv', 'rb')
csv2 = open('Test_Matrix_csv_test_intensity.csv', 'rb')
cluster_list = r"NN_ALL_ASSIGN_p-0.8_a-300_b-300_c-0.1_theta-0.15_count-20.txt"
file = open(cluster_list)


d_list = {}
d_intensity = {}
d_stitched = {}
d_name = {}
Burst_Hold = []
Cluster_Hold = []
len_row1 = 0
len_row2 = 0
row_num1 = 0
row_num2 = 0
row_num3 = 0
max_index = 0

colors = [r'b', r'g',  r'r', r'c', r'm', r'k', r'y']

hclust = True


for i in file:
    a = i.strip("\n")
    b = a.strip()    
    Cluster_Hold.append(int(b.split()[-1]))
    if hclust == True:
        Burst_Hold.append(b[-7:-2].strip("r").strip("_").strip("\""))

    if hclust == False:
        Burst_Hold.append(b[-6:-3].strip("_").strip("r").strip("\""))
    


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
    for x in range(1, int(max_index)+1):
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


    
fig, ax = plt.subplots()
ax.plot(d_stitched["Burstx"+str(series)], d_stitched["Bursty"+str(series)], 'b-')
ax.set_xlabel('Frame')
ax.set_ylabel('Intensity', color='k')
ax.tick_params('y', colors='k')
    
plt.show(block=False)




fig = plt.figure()
ax1 = fig.add_subplot(111)


for i in range(1,len(d_name)+1):
    for x in range(1, int(max_index)+1):
        if int(d_name["Burst"+str(i)][0]) == series:
            ax1.plot(d_list["Burst"+str(int(d_name["Burst"+str(i)][1]))],
                           d_intensity["Burst"+str(int(d_name["Burst"+str(i)][1]))],
                           c=str(colors[Cluster_Hold[int(d_name["Burst"+str(i)][1])]]),
                           label=str(Cluster_Hold[int(d_name["Burst"+str(i)][1])]))
            ax1.set_xlabel('Frame')
            ax1.set_ylabel('Intensity', color='k')
            ax1.tick_params('y', colors='k')
            
            
            break

clust1 = mpatches.Patch(color='b', label='Clust 1')
clust2 = mpatches.Patch(color='g', label='Clust 2')
clust3 = mpatches.Patch(color='r', label='Clust 3')
clust4 = mpatches.Patch(color='c', label='Clust 4')
clust5 = mpatches.Patch(color='m', label='Clust 5')
plt.legend(handles=[clust1, clust2, clust3, clust4, clust5],prop={'size':6})

plt.show()
plt.clf()
plt.close()




