import csv
import numpy as np
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
import heapq, random



f = open('Lottery_Powerball_Winning_Numbers__Beginning_2010.csv')
csv_f = csv.reader(f)

numbers = []

for line in csv_f:
    temp = line[1].split()

    for i in temp:
        numbers.append(i)

numbers = numbers[2:]

numbers_int = []
for i in numbers:
    numbers_int.append(int(i))

print '-------------Actual value-------------'
print "Mean: ", np.mean(numbers_int[3924:])
print "Median: ", np.median(numbers_int[3924:])
print "This is a strange result"
print
print "STD: ", np.std(numbers_int[3924:])

print numbers_int[3924:]
temp = 0
temp2 = []
temp3 = []
for i in range(1,70):
    temp3.append(i)
    temp2.append(i/float(69))

print
print '-----------statistical value-----------'

print "Mean: ", sum(temp2)
print "Median: ", np.median(temp3)
print "STD: ", np.std(temp3)

average_individual = []
end_numbers = []
average_individual2 = []

for n in range(0, len(numbers)):
    if n%6 == 0:
        temp1 = int(numbers[n])
        temp2 = int(numbers[n+1])
        temp3 = int(numbers[n+2])
        temp4 = int(numbers[n+3])
        temp5 = int(numbers[n+4])
        temp6 = int(numbers[n+5])

        average_individual2.append(temp1)
        average_individual2.append(temp2)
        average_individual2.append(temp3)
        average_individual2.append(temp4)
        average_individual2.append(temp5)
        #average_individual2.append(temp6)

        end_numbers.append(temp6)
        n = [temp1, temp2, temp3, temp4, temp5]
        average_individual.append(np.mean(n))

print
print '---Actual Mean Value (for every set)---'

print "Mean: ", np.mean(average_individual)
print "Due to the limitation of one number not being able to be drawn twice"
print "This establishes that the mean as calculated above is correct"

print stats.mode(numbers_int)

print average_individual2
print len(average_individual2)
average_individual2 = average_individual2[3265:]
print len(average_individual2)

id_count = []
average_count = []
for i in range(1,70):
    average_individual2.count(i)
    #if numbers_int.count(i) > 65:
        #print "Number ", i, ": ", numbers_int.count(i)
    average_count.append(int(average_individual2.count(i)))
    id_count.append(int(i))

print
print "Most likely numbers (times picked, numbers below):"
A = heapq.nlargest(6, average_count)
print A

for i in range(0,69):
    if average_count[i] in A:
        print i+1, average_count[i]


plt.plot(id_count, average_count)
plt.show()


B = heapq.nlargest(6, end_numbers)

id_end_numbers = []
id_end_count = []
for i in range(1,70):
    end_numbers.count(i)
    #print "Number ", i, ": ", numbers_int.count(i)
    id_end_count.append(int(numbers_int.count(i)))
    id_end_numbers.append(int(i))



print len(end_numbers[654:])
end_numbers = end_numbers[654:]


id_end_count = []
average_end_count = []
for i in range(1,70):
    end_numbers.count(i)
    #if numbers_int.count(i) > 65:
    #print "Number ", i, ": ", end_numbers.count(i)
    average_end_count.append(int(end_numbers.count(i)))
    id_end_count.append(int(i))

print
print "Most likely Poweball (times picked, numbers below):"
B = heapq.nlargest(6, average_end_count)
print B

for i in range(0,69):
    if average_end_count[i] in B:
        print i+1, average_end_count[i]





plt.plot(id_end_count,average_end_count )
plt.show()


