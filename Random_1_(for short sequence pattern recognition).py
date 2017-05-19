from matplotlib import *
import matplotlib.pyplot as plt
from numpy import *
from scipy import stats

#import and sort data file into list of base pairs
list = ["g","g","u","t","c","c","u","g","g","u","t","c","g","g","g","c","g",
        "g","g","u","g","g","u","t","c","c","g","g","g","u","g","g","u","t",
        "c","g","g","u","g","g","u","c","g","g","g","u","t","c","c","g","g",
        "g","u","g","g","u","t","c","c","g","g","g","u","g","g","u","t","c",
        "c","g"]

#Adds to end of list to make the next section work to find pattern
list.append("X"); list.append("X");list.append("X"); list.append("X")


number = [i for i in range(0, len(list)-4)]

List_Number_Hold = 0
d_Find = {}

for i in range(0,len(list)):
    if list[i] == 'g':
        if list[i+1] == 'g':
            if list[i+2] == 'u':
                #if list[i+3] == 'u':
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
            distance_forward_back.append((d_Distance["Distance_back" + str(i)]), (d_Distance["Distance_forward" + str(i)]))
    if d_Distance.has_key("Distance_forward"+str(i)) is True:
        if d_Distance.has_key("Distance_back" + str(i)) is False:
            #Check Tuple Creation
            distance_forward_back.append(0, (d_Distance["Distance_forward" + str(i)]))
    if d_Distance.has_key("Distance_forward"+str(i)) is False:
        if d_Distance.has_key("Distance_back" + str(i)) is True:
            #Check Tuple Creation
            distance_forward_back.append((d_Distance["Distance_back" + str(i)]),0)


print distance_forward_back
distance_forward = distance_forward_back[:,1]
distance_back = distance_forward_back[:,0]

for i in range(0, (len(d_Distance.keys()))/2 + 1):
    #Check syntax
    if distance_forward_back[i,0] > 5:
        print "Distance Forward for", i, "Match:", distance_forward_back[i,0]
    if distance_forward_back[i,1] > 5:
        print "Distance Back for", i, "Match:", distance_forward_back[i,0]
        print distance_forward_back[i,0]


numbers_true = []

for i in range(0,len(number)):
    if i in print_list:
        numbers_true.append(1)
    if i not in print_list:
        numbers_true.append(0)



print "Mean distance forward:", np.mean(distance_forward[1:])
#Check to insure the last digit is indeed leaving off the last zero 0 with -1
print "Median distance forward:", np.median(distance_forward[:-1])
print "STD distance forward:", np.std(distance_forward[1:])
print "Probability of sequence occuring: 1 /", 4**4
print
print "Mode distance forward:", stats.mode(numbers_int)

distance_count = []
distance_count_number = []

for i in range(0,int(max(distance_forward[:]))+5):
    distance_forward.count(i)
    distance_count.append(int(end_numbers.count(i)))
    distance_count_number.append(int(i))
    

plt.plot(distance_count_number, distance_count)
plt.show(block=False)


plt.plot(number, numbers_true)
plt.show()
