import csv
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
import pyrenn as prn

csv_file = r"training_data_unnormalized_ccf.csv"

row_temp = []
dc1_p = []
dc2_p = []
G_t = []

header_save = 0
with open(csv_file, 'rb') as f:
    next(f)
    reader = csv.reader(f)
    for row in reader:
        row_temp.append(float(row[0]))
        dc1_p.append(float(row[1]))
        dc2_p.append(float(row[2]))
        G_t.append(float(row[3]))

    header_save = 1

fig, ax1 = plt.subplots()
ax1.plot(row_temp, dc1_p, 'g-')
ax2 = ax1.twinx()
ax2.plot(row_temp, dc2_p, 'r')
#plt.show()
plt.clf()
plt.close()

dc1_p_temp = []
for i in range(0,len(dc1_p[:])):
    temp = (dc1_p[i] - min(dc1_p)) / (max(dc1_p) - min(dc1_p))
    dc1_p_temp.append(temp)
dc1_p = dc1_p_temp


dc2_p_temp = []
for i in range(0,len(dc2_p[:])):
    temp = (dc2_p[i] - min(dc2_p)) / (max(dc2_p) - min(dc2_p))
    dc2_p_temp.append(temp)
dc2_p = dc2_p_temp



row_temp = np.array(row_temp)
dc1_p = np.array(dc1_p)
dc2_p = np.array(dc2_p)
G_t = np.array(G_t)

print dc1_p

net = prn.CreateNN([1,13,20,1])

net = prn.train_LM(dc1_p,G_t,net,verbose=True,k_max=1000,dampfac=.2,dampconst=5,E_stop=1e-5)




csv_file_training = r"training_data_unnormalized.csv"


row_temp_training = []
dc1_p_training = []
dc2_p_training = []
G_t_training = []

with open(csv_file_training, 'rb') as f:
    next(f)
    reader = csv.reader(f)
    for row in reader:
        row_temp_training.append(float(row[0]))
        dc1_p_training.append(float(row[1]))
        dc2_p_training.append(float(row[2]))
        G_t_training.append(float(row[3]))

fig, ax1 = plt.subplots()
ax1.plot(row_temp_training, dc1_p_training, 'g-')

ax2 = ax1.twinx()
ax2.plot(row_temp_training, dc2_p_training, 'r')
plt.show()
plt.clf()
plt.close()


row_temp_training = np.array(row_temp_training)
dc1_p_training = np.array(dc1_p_training)
dc2_p_training = np.array(dc2_p_training)
G_t_training = np.array(G_t_training)


G_t_predict = prn.NNOut(dc1_p,net)

print G_t_predict

print G_t
fig, ax1 = plt.subplots()
ax1.plot(row_temp, G_t, 'b-')

ax2 = ax1.twinx()
ax2.plot(row_temp, G_t_predict, 'r')
plt.show()
plt.clf()
plt.close()
