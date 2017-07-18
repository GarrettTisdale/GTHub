import os
import sys
import csv
import string
import xlsxwriter
import numpy as np
import os, fnmatch
import matplotlib as mp
import matplotlib.pyplot as plt


path1 = r'C:\Users\tisdalege\Desktop\Reorganized Data\_Treatment Data\vehicle_DATA'
folder = r'\Only_Data'

#Number of the Last Burst Given
combind_burst_num = 0

data_set_name = 'Data_'
data_set_number = 3


csv_name1 = r'3_Test_Matrix_csv_test_intensity.csv'
csv_name2 = r'3_Test_Matrix_csv_test_frames.csv'


trk_list = []
trk_list_ordered = []

marker_1 = 3


di=dict(zip(string.letters,[ord(c)%32 for c in string.letters]))

test = r"31b_209_Eth_p4_cell5_cropped.SubFF122.trk"

print test[13]


def findFiles(path1, folder, filter):
    for root, dirs, files in os.walk(path1):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(file)


for trkFile in findFiles(path1, folder, '*.trk'):
    trk_list.append(trkFile)
    

for i in trk_list:   
    for x in range(0,10):
        if int(i[13]) == x:
            #temp = temp[4:7]
            if '_R' in i:
                temp = str(int(float(i[0:2]))) + str('.') + str(di[i[2]]) + str(x) + str(i[19])
            else:
                temp = str(int(float(i[0:2]))) + str('.') + str(di[i[2]]) +  str(x) + str(i[19])
            
    trk_list_ordered.append(temp)
    
print trk_list_ordered

forward = True
end_list = []


def enumerate(trk_list, forward):
    global trk_list_ordered
    global end_list
    constant = -1
    end_list1 = []
    end_list2 = []
    
    identity_list = []
    
    for i in trk_list:
        constant = constant + 1
        identity_list.append(constant)  
        for x in range(0,10):
            if int(i[13]) == x:
                #temp = temp[4:7]
                if '_R' in i:
                    temp = str(int(float(i[0:2]))) + str('.') + str(di[i[2]]) + str(x) + str(i[19])
                else:
                    temp = str(int(float(i[0:2]))) + str('.') + str(di[i[2]]) +  str(x) + str(i[19])
                
                end_list1.append(float((temp)))
    
    source = []

    if forward is False:
        for j in range(0, len(identity_list)):
            for i in identity_list:
                if i >= 0:
                    if end_list1[i] is max(end_list1):
                        if end_list1[i] >= 0:
                            source.append(trk_list[i])
                            end_list2.append(end_list1[i])
                            end_list1[i] = -1
                            identity_list[i] = -1

    if forward is True:
        for j in range(0, len(identity_list)):
            for i in identity_list:
                if i >= 0:
                    if end_list1[i] is min(end_list1):
                        if end_list1[i] >= 0:
                            source.append(trk_list[i])
                            end_list2.append(end_list1[i])
                            end_list1[i] = 9999
                            identity_list[i] = -1
    end_list = end_list2
    trk_list_ordered = source


enumerate(trk_list, forward)

print end_list

length_list = []

d_matrix_hold = {}


burst_count_number_img = combind_burst_num
burst_count_number_img_view = combind_burst_num + 1
burst_count_number_index = []
trk_count = 0

for x in trk_list_ordered:
    path = path1
    file = x
    file2 = x.strip('.trk')+'_idealized_traces.txt'


    if sys.platform == 'win32':
        tempslash = "\\"
    else:  # sys.platform=='darwin':
        tempslash = "//"


    Intensity = []
    Frame = []
    HMM = []
    
    
    for i in open(path+tempslash+file, 'r'):
        y = i.split(',')
        x = y[0].split()
        for y in x:
            if y == x[2]:
                Intensity.append(y)
            if y == x[3]:
                Frame.append(y)
    
    
    for i in open(path+tempslash+file2, 'r'):
        HMM.append(int(float(i.strip('\n'))))
    HMM.append(int(0))
    
    
    HMM_temp = []
    for i in HMM:
        if i == max(HMM):
            HMM_temp.append(1)
        else:
            HMM_temp.append(0)

    HMM = HMM_temp

    if len(Frame) != len(Intensity):
        Frame = Frame[1:len(Intensity)+1]
    if len(HMM) != len(Intensity):
        HMM = HMM[0:len(Intensity)]
    
    
    d_List = {}
    hold = 0
    
    
    for i in range(1,len(HMM)-1):
        if HMM[i] == 1:
            if HMM[i-1] == 0:
                d_List["Burst{0}".format(hold)] = []
                a =  d_List["Burst" + str(hold)]
                
                d_List["Intensity{0}".format(hold)] = []
                b =  d_List["Intensity" + str(hold)]
                
                d_List["Frame{0}".format(hold)] = []
                c =  d_List["Frame" + str(hold)]
                
                if i not in range(1, 5):
                    a.append(int(0))
                    a.append(int(0))
                    a.append(int(0))
                    
                    
                    b.append(Intensity[i-4]);b.append(Intensity[i-3]);b.append(Intensity[i-2])
                    c.append(Frame[i-4]);c.append(Frame[i-3]);c.append(Frame[i-2])
    
    
                a.append(int(1))
                b.append(Intensity[i-1])
                c.append(Frame[i-1])
                
                
            if HMM[i-1] == 1:            
                if i == range(1,len(HMM)-1)[-1]:
                    print
                if i is not range(1,len(HMM)-1)[-1]:
                    if len(d_List) == 0:
                        d_List["Burst{0}".format(hold)] = []
                        a =  d_List["Burst" + str(hold)]
                        d_List["Intensity{0}".format(hold)] = []
                        b =  d_List["Intensity" + str(hold)]
                        d_List["Frame{0}".format(hold)] = []
                        c =  d_List["Frame" + str(hold)]
                        
                        a.append(int(1))
                        b.append(Intensity[i-1])
                        c.append(Frame[i-1])
                    else:
                        a =  d_List["Burst" + str(hold)]
                        b =  d_List["Intensity" + str(hold)]
                        c =  d_List["Frame" + str(hold)]
                        
                        a.append(int(1))
                        b.append(Intensity[i-1])
                        c.append(Frame[i-1])
                    if HMM[i+1] == 0:
                        if i not in range(len(HMM)-5, len(HMM)-1):
                            a.append(int(0))
                            a.append(int(0))
                            a.append(int(0))
                            
                            b.append(Intensity[i+1]);b.append(Intensity[i+2]);b.append(Intensity[i+3])
                            c.append(Frame[i+1]);c.append(Frame[i+2]);c.append(Frame[i+3])
                                
                        hold = hold + 1
                        
    if len(Frame) != len(HMM):
        HMM.append(int(1))


    fig, ax1 = plt.subplots()
    
    ax1.plot(Frame, Intensity, 'b-')
    ax1.set_xlabel('Frame')
    ax1.set_ylabel('Intensity', color='b')
    ax1.tick_params('y', colors='b')
    
    ax2 = ax1.twinx()
    
    ax2.plot(Frame, HMM, 'r--')
    ax2.set_ylabel('HMM', color='r')
    ax2.tick_params('y', colors='r')
    
    fig.savefig(file.strip('.trk')+'.png')
    
    plt.clf()
    plt.close()
    
    
    len_burst = []
    
    for i in range(0, len(d_List)/3):
        if len(d_List['Frame'+str(i)]) >= 1:
#            if len(d_List['Frame'+str(i)]) <= 30:
#            if len(d_List['Frame'+str(i)]) != 20:
#                print d_List['Intensity'+str(i)]
#                fig, ax = plt.subplots()
#                ax.plot(d_List['Frame'+str(i)], d_List['Intensity'+str(i)], 'b-')
#                ax.set_xlabel('Frame')
#                ax.set_ylabel('Intensity', color='b')
#                ax.tick_params('y', colors='b')
#                    
#                fig.savefig(file.strip('.trk')+ "_Burst_" +str(burst_count_number_img)+'.png')
#                plt.clf()
#                plt.close()


            #if len(d_List['Frame'+str(i)]) == 20:
            fig, ax = plt.subplots()
            ax.plot(d_List['Frame'+str(i)], d_List['Intensity'+str(i)], 'b-')
            ax.set_xlabel('Frame')
            ax.set_ylabel('Intensity', color='b')
            ax.tick_params('y', colors='b')
                
            fig.savefig(file.strip('.trk')+ "_RANGE_Burst_" +str(burst_count_number_img_view)+'.png')

            plt.clf()
            plt.close()

            Burst_Name = data_set_name+ str(data_set_number) + str("_") + str(end_list[trk_count]) + '_Burst_Number_' + str(burst_count_number_img_view)

            burst_count_number_index.append(burst_count_number_img_view)
            d_matrix_hold["Burst_Name_{0}".format(burst_count_number_img_view)] = Burst_Name
           
            int_hold1 = []
            int_hold2 = []
            
            for z in range(0, len(d_List['Frame'+str(i)])):
                int_hold1.append(d_List['Frame'+str(i)][z])
                int_hold2.append(d_List['Intensity'+str(i)][z])
            
            for z in range(len(d_List['Frame'+str(i)]), 400):
                int_hold1.append("")
                int_hold2.append("")

                
            data_matrix_temp = np.column_stack((int_hold1, int_hold2))
            d_matrix_hold["Data_burst{0}".format(burst_count_number_img_view)] = data_matrix_temp
            burst_count_number_img_view = burst_count_number_img_view + 1
    trk_count += 1

Header_Row = []
element_hold = 1
matrix1 = np.array(element_hold)
matrix2 = np.array(element_hold)
header_array = np.array(element_hold)



for i in range(0, len(burst_count_number_index)):
    Header_Row.append(d_matrix_hold["Burst_Name_"+str(burst_count_number_index[i])])
    header_array = np.asarray(Header_Row)
    
for i in range(combind_burst_num+1, burst_count_number_img_view):
    if i == combind_burst_num+1:
        matrix1 = np.array(d_matrix_hold["Data_burst"+str(i)][:,1])
        matrix2 = np.array(d_matrix_hold["Data_burst"+str(i)][:,0])


    if i > combind_burst_num+1:
        matrix1 = np.vstack((matrix1, np.array(d_matrix_hold["Data_burst"+str(i)][:,1])))
        matrix2 = np.vstack((matrix2, np.array(d_matrix_hold["Data_burst"+str(i)][:,0])))


with open(csv_name1, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(np.vstack((header_array, matrix1.transpose())))


with open(csv_name2, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(np.vstack((header_array, matrix2.transpose())))

