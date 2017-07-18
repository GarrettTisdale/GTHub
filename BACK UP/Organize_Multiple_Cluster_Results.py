import os
import sys
import csv
import glob
import xlsxwriter
import numpy as np
import os, fnmatch
import matplotlib as mp
import matplotlib.pyplot as plt
directory = r"C:\Users\tisdalege\Desktop\Reorganized Data\1_Workspace\DTW_Workspace_Results_1"


txt_list = []
txt_list_ordered = []
txt_list2 = glob.glob(directory + '/*.txt')

for i in txt_list2:
    txt_list.append(i.split('\\')[-1])



for i in txt_list:
    if "stage2" in i:
        if "Number" not in i:
            for x in range(0,20):
                if int(i[27]) == x:
                    temp = i[17] + str('.') + str(x)
                    txt_list_ordered.append(temp)
    
    
forward = True
end_list = []


def enumerate(txt_list, forward):
    global txt_list_ordered
    global end_list
    constant = -1
    update_list = []
    end_list1 = []
    end_list2 = []
    
    identity_list = []
    
    for i in txt_list:  
        if "stage2" in i:
            if "Number" not in i:
                for x in range(0,20):
                    if int(i[27]) == x:
                        update_list.append(i)
                        constant = constant + 1
                        identity_list.append(constant)
                        temp = i[17] + str('.') + str(x)
                        end_list1.append(float((temp)))
    source = []

    if forward is False:
        for j in range(0, len(identity_list)):
            for i in identity_list:
                if i >= 0:
                    if end_list1[i] is max(end_list1):
                        if end_list1[i] >= 0:
                            source.append(update_list[i])
                            end_list2.append(end_list1[i])
                            end_list1[i] = -1
                            identity_list[i] = -1

    if forward is True:
        for j in range(0, len(identity_list)):
            for i in identity_list:
                if i >= 0:
                    if end_list1[i] is min(end_list1):
                        if end_list1[i] >= 0:
                            source.append(update_list[i])
                            end_list2.append(end_list1[i])
                            end_list1[i] = 9999
                            identity_list[i] = -1
    end_list = end_list2
    txt_list_ordered = source


enumerate(txt_list, forward)


cumulative_sum_of_clusters = 0

cluster_list_name = []
cluster_list_number = []

for i in txt_list_ordered:
    if sys.platform == 'win32':
        tempslash = "\\"
    else:  # sys.platform=='darwin':
        tempslash = "//"
    f = open(directory+tempslash+i)
    
    
    for x in f:
        name =  x.strip("\n").split()[0]
        cluster = float(x.strip("\n").split()[1]) + cumulative_sum_of_clusters
        
        if name not in cluster_list_name:
            cluster_list_number.append(cluster)
            cluster_list_name.append(name)
    
    cumulative_sum_of_clusters = max(cluster_list_number)
        


cluster_list_ordered_name = []
cluster_list_ordered_number = []






def enumerate_clusters(cluster_list_name, cluster_list_number, forward):
    global cluster_list_ordered_name
    global cluster_list_ordered_number
    constant = -1
    update_list1 = []
    update_list2 = []
    end_list1 = []
    end_list2 = []
    
    identity_list = []
    
    for i in range(0,len(cluster_list_name)):  
        update_list1.append(cluster_list_name[i])
        update_list2.append(cluster_list_number[i])
        
        constant = constant + 1
        identity_list.append(constant)
        temp = cluster_list_name[i][-4:].strip("e").strip("r").strip("_")

        end_list1.append(float((temp)))

    
    source1 = []
    source2 = []

    if forward is False:
        for j in range(0, len(identity_list)):
            for i in identity_list:
                if i >= 0:
                    if end_list1[i] is max(end_list1):
                        if end_list1[i] >= 0:
                            source1.append(update_list1[i])
                            source2.append(int(float(update_list2[i])))
                            end_list2.append(end_list1[i])
                            end_list1[i] = -1
                            identity_list[i] = -1


    if forward is True:
        for j in range(0, len(identity_list)):
            for i in identity_list:
                if i >= 0:
                    if end_list1[i] is min(end_list1):
                        if end_list1[i] >= 0:
                            source1.append(update_list1[i])
                            source2.append(int(float(update_list2[i])))
                            
                            end_list2.append(end_list1[i])
                            end_list1[i] = 9999
                            identity_list[i] = -1

    cluster_list_ordered_name = source1
    cluster_list_ordered_number = source2



enumerate_clusters(cluster_list_name, cluster_list_number, forward)

longest_length = len(cluster_list_name[-1])

matrix = np.column_stack((np.array(cluster_list_ordered_name),np.array(cluster_list_ordered_number)))


print matrix

np.savetxt('FullTest_kc_stage2_All_Ordered_Clusters.txt', matrix, delimiter=" ", fmt="%-{0}s".format(longest_length)) 






