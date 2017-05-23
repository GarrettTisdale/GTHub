from matplotlib import *
import matplotlib.pyplot as plt
from numpy import *
import numpy as np
from scipy import stats

#import and sort data file into list of base pairs
file_hold = []



for z in file_hold:
    list = []
    for i in open(z,"r"):
        for x in i:
            list.append(x)
        
    
    #for i in open(file_hold[0]):
    #    for x in i:
    #        list.append(x)
    
    
                
    #Adds to end of list to make the next section work to find pattern
    list.append("X"); list.append("X");list.append("X"); list.append("X")
    
    
    number = [i for i in range(0, len(list)-4)]
    
    List_Number_Hold = 0
    d_Find = {}
    
    for i in range(0,len(list)):
        if list[i] == '':
            if list[i+1] == '':
                if list[i+2] == '':
                    if list[i+3] == '':
                        d_Find["Find{0}".format(List_Number_Hold)] = i
                        List_Number_Hold = List_Number_Hold + 1
    
    
    #Deletes added ending
    for i in list[-4:]:
        del list[-1]
    
    
    print_list = []
    locations_Find = []
    
    #formatted to list not location
    d_Distance = {}
    #forward is listed as: d_Distance{0} [back,forward]
    distance_forward_back = []
    
    for i in range(0,len(d_Find.keys())):
        locations_Find.append(d_Find["Find"+str(i)])
        print_list.append(d_Find["Find"+str(i)])
        if d_Find.has_key("Find"+str(i+1)) is True:
            d_Distance["Distance_forward{0}".format(i)] = (d_Find["Find"+str(i+1)]) - (d_Find["Find"+str(i)])
        if d_Find.has_key("Find"+str(i-1)) is True:
            d_Distance["Distance_back{0}".format(i)] = (d_Find["Find" + str(i)]) - (d_Find["Find" + str(i-1)])
    
    for i in range(0, (len(d_Distance.keys()))/2 + 1):
        if d_Distance.has_key("Distance_forward"+str(i)) is True:
            if d_Distance.has_key("Distance_back" + str(i)) is True:
                #Check Tuple Creation
                temp = [(d_Distance["Distance_back" + str(i)]), (d_Distance["Distance_forward" + str(i)])]
                distance_forward_back.append(temp)
        if d_Distance.has_key("Distance_forward"+str(i)) is True:
            if d_Distance.has_key("Distance_back" + str(i)) is False:
                #Check Tuple Creation
                temp = [0, (d_Distance["Distance_forward" + str(i)])]
                distance_forward_back.append(temp)
        if d_Distance.has_key("Distance_forward"+str(i)) is False:
            if d_Distance.has_key("Distance_back" + str(i)) is True:
                #Check Tuple Creation
                temp = [(d_Distance["Distance_back" + str(i)]),0]
                distance_forward_back.append(temp)
    
    
    distance_forward = []
    distance_back = []
    
    for x in distance_forward_back:
        distance_back.append(x[0])
        distance_forward.append(x[1])
    
    
    
    
    #for i in range(0, (len(d_Distance.keys()))/2 + 1):
        #Check syntax
        #if distance_forward_back[i][0] > 0:
            #print "Distance Forward for", i, "Match:", distance_forward_back[i][0]
        #if distance_forward_back[i][1] > 0:
            #print "Distance Back for", i, "Match:", distance_forward_back[i][0]
    
    
    numbers_true = []
    
    for i in range(0,len(number)):
        if i in print_list:
            numbers_true.append(1)
        if i not in print_list:
            numbers_true.append(0)
    
    
    distance_count = []
    distance_count_number = []
    
    for i in range(0,int(max(distance_forward[:]))+5):
        distance_forward.count(i)
        distance_count.append(int(distance_forward.count(i)))
        distance_count_number.append(int(i))
    
    count_track = []
    number_of = 0
    
    
    for i in range(0, len(distance_count)):
        if distance_count[i] is not 0:
            count_track.append(distance_count_number[i])
            number_of = number_of + distance_count[i]
    
    
    #plt.plot(distance_count_number, distance_count)
    #plt.show(block=True)
    
    
    #plt.plot(number, numbers_true)
    #plt.show()
    
    
    
    new_plot_x = []
    new_plot_y = []
    
    hold_number = 0
    count_hold = 0
    
    
    for i in count_track:
        if i <= hold_number:
            count_hold = count_hold + 1
        else:
            new_plot_x.append(hold_number)
            new_plot_y.append(count_hold)
            
            count_hold = 0
            hold_number = hold_number + 50
    
    #plt.plot(new_plot_x, new_plot_y)
    #plt.show()
    
    
    print "Mean distance forward:", np.mean(distance_forward)
    #Check to insure the last digit is indeed leaving off the last zero 0 with -1
    print "Median distance forward:", np.median(distance_forward)
    print "STD distance forward:", np.std(distance_forward)
    print "Probability of sequence occuring: 1 /", 4**4
    print "Theoretically probably number:", len(list)/4**4
    print "Actual number found:", number_of
    print
    
    
    
    plt.hist(count_track, bins=65)
    plt.show()



