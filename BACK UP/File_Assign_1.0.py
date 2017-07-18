import os
import fnmatch
import shutil
from shutil import copyfile

path = r'C:\Users\tisdalege\Desktop\Reorganized Data\3_Workspace'
file_name = r'\FullTest_kc_stage2_All_Ordered_Clusters.txt'
#file_extension = file_name[-45:-3]
new_folder = r'\DTW'
sub_folder = r'\Test 1' #+ file_extension


file = open(path+file_name)


hclust = True


Burst_Hold = []
Cluster_Hold = []



for i in file:
    a = i.strip("\n")
    b = a.strip()    
    Cluster_Hold.append(int(b.split()[-1]))
    if hclust == True:
        Burst_Hold.append(b[-7:-1].strip("r").strip("_").strip("\"").split()[0])

    if hclust == False:
        Burst_Hold.append(b[-6:-3].strip("_").strip("r").strip("\""))
    

number_of_clusters = max(Cluster_Hold)
                               
print Cluster_Hold                     

def findFiles(path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(file)

png_List = []

for pngFile in findFiles(path+"\ImageFolder", '*.png'):
    a = pngFile[-23:-4]
    #print a
    
    if '_' in a[0:3]:
        a = a.replace("_", "", 1)
    if '_' in a[0:3]:
        a = a.replace("_", "", 1)
    if '0' in a[0:3]:
        a = a.replace("0", "", 1)
    if '1' in a[0:3]:
        a = a.replace("1", "", 1)
    if '2' in a[0:3]:
        a = a.replace("2", "", 1)
    if '3' in a[0:3]:
        a = a.replace("3", "", 1)
    
    if "Burst_" in a:
        png_List.append("\\"+pngFile)

for i in range(1, int(number_of_clusters)+1):
    Cluster = r"\Cluster {0}" 
    if not os.path.exists(path+new_folder+sub_folder+Cluster.format(i)):
        os.makedirs(path+new_folder+sub_folder+Cluster.format(i))



for i in range(0, len(Burst_Hold)):
    for x in range(0, len(png_List)):
        if "RANGE_Burst_{0}.png".format(str(int(Burst_Hold[i]))) in png_List[x]:
            cluster = Cluster_Hold[i]
            print path+png_List[x]
            Cluster = r"\Cluster {0}" 

            shutil.copy(path+"\Imagefolder"+png_List[x], path+new_folder+sub_folder+Cluster.format(str(cluster)))
            
            break
        
          