from matplotlib import *
import matplotlib.pyplot as plt
from numpy import *

#import and sort data file into list of base pairs
list = ["g","g","u","t","c","c","u","g","g","u","t","c","g","g","g","c","g","g","g","u","g","g","u","t","c","c","g","g",
        "g","u","g","g","u","t","c","g", "g", "u","g","g","u","c","g","g","g","u","t","c","c","g","g","g","u",
        "g", "g", "u", "t", "c", "c", "g","g","g","u", "g","g","u","t","c","c","g"]

#Adds to end of list to make the next section work to find pattern
list.append("X"); list.append("X");list.append("X"); list.append("X")


number = [i for i in range(0, len(list)-4)]

List_Number_Hold = 0
d_Find = {}

for i in range(0,len(list)):
    if list[i] == 'g':
        if list[i+1] == 'g':
            if list[i+2] == 'u':
                d_Find["Find{0}".format(List_Number_Hold)] = i
                List_Number_Hold = List_Number_Hold + 1


#Deletes added ending
for i in list[-4:]:
    del list[-1]


print_list = []
locations_Find = []

#formatted to list not location
d_Distance = {}


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
            print (d_Distance["Distance_back" + str(i)]), (d_Distance["Distance_forward" + str(i)])
    if d_Distance.has_key("Distance_forward"+str(i)) is True:
        if d_Distance.has_key("Distance_back" + str(i)) is False:
            print "0", (d_Distance["Distance_forward" + str(i)])
    if d_Distance.has_key("Distance_forward"+str(i)) is False:
        if d_Distance.has_key("Distance_back" + str(i)) is True:
            print (d_Distance["Distance_back" + str(i)]), "0"

numbers_true = []

for i in range(0,len(number)):
    if i in print_list:
        numbers_true.append(1)
    if i not in print_list:
        numbers_true.append(0)

plt.plot(number, numbers_true)
plt.show()
