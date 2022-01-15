import os
import sys
import numpy as np
import h5py
from plyfile import PlyData, PlyElement
import matplotlib.pyplot as plt
import json
from mpl_toolkits.mplot3d import Axes3D
import provider
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)


#code from raw data
seg_name=[]
seg_label=[]
for root, dirs, files in os.walk('./part_seg/PartAnnotation/02691156/expert_verified/points_label'):
    for fname in files:
        full_fname = os.path.join(root, fname)
        #print(fname[:-4])
        f = open(full_fname, 'r')
        line = f.readlines()
        f.close()
        #print(len(line))
        seg_label=seg_label+[line]
        seg_name = seg_name+[fname[:-4]]

temp=[]
temp_p=[]
for root, dirs, files in os.walk('./part_seg/PartAnnotation/02691156/points'):
    for fname in files:
        full_fname = os.path.join(root, fname)
        f = open(full_fname, 'r')
        line = f.readlines()
        f.close()
        temp_p=temp_p+[line]
        temp = temp + [fname[:-4]]

points=[]
for filename in seg_name:
    if filename in temp:
        points=points+[temp_p[temp.index(filename)]]

#print(len(points))
#print(seg_label)
for i in range(len(points)):
    for j in range(len(points[i])):
        points[i][j]=points[i][j].split(' ')
maxmin=[]
for i in range(len(points)):
    max_x=-10
    min_x=10
    max_y=-10
    min_y=10
    max_z=-10
    min_z=10

    for j in range(len(points[i])):
        points[i][j][0]=float(points[i][j][0])
        points[i][j][1] = float(points[i][j][1])
        points[i][j][2] = float(points[i][j][2])
        seg_label[i][j] = int(seg_label[i][j])
        if points[i][j][0]>=max_x:
            max_x=points[i][j][0]
        if points[i][j][1]>=max_y:
            max_y=points[i][j][1]
        if points[i][j][2]>=max_z:
            max_z=points[i][j][2]
        if points[i][j][0]<=min_x:
            min_x=points[i][j][0]
        if points[i][j][1]>=max_y:
            min_y=points[i][j][1]
        if points[i][j][2]>=max_z:
            min_z=points[i][j][2]
    maxmin=maxmin+[[max_x,min_x,max_y,min_y,max_z,min_z]]
#print(len(points))
#print(points[i])
#print(seg_name[0])

result={}
for i in range(len(points)):
    local_max=max(maxmin[i])
    local_min=min(maxmin[i])
    result[seg_name[i]]={"seg_label" : seg_label[i], "points" : points[i], "max_x" : maxmin[i][0], "min_x" : maxmin[i][1],"max_y" : maxmin[i][2],"min_y" : maxmin[i][3],"max_z" : maxmin[i][4],"min_z" : maxmin[i][5],"local_max" : local_max, "local_min" : local_min}

with open('airplane_result.json', 'w') as fp:
    json.dump(result, fp)


sample=result["1a04e3eab45ca15dd86060f189eb133"]

X=[i[0] for i in sample["points"]]
Y=[i[1] for i in sample["points"]]
Z=[i[2] for i in sample["points"]]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X,Y,Z)
ax.set_xlim3d(sample["local_min"]-0.1,sample["local_max"]+0.1 )
ax.set_ylim3d(sample["local_min"]-0.1,sample["local_max"]+0.1 )
ax.set_zlim3d(sample["local_min"]-0.1,sample["local_max"]+0.1 )
plt.show()


"""
#expert validate data only
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

TRAIN_FILES = provider.getDataFiles( \
    os.path.join(BASE_DIR, 'part_seg/hdf5_data/train_hdf5_file_list.txt'))
TEST_FILES = provider.getDataFiles(\
    os.path.join(BASE_DIR, 'part_seg/hdf5_data/test_hdf5_file_list.txt'))
#EVAL_FILES = provider.getDataFiles(\
#    os.path.join(BASE_DIR< 'part_seg/hdf5_data/val_hdf5_file_list.txt'))
ALL_FILES = provider.getDataFiles( \
    os.path.join(BASE_DIR, 'part_seg/hdf5_data/train_hdf5_file_list.txt'))
ALL_FILES = ALL_FILES + provider.getDataFiles(\
    os.path.join(BASE_DIR, 'part_seg/hdf5_data/test_hdf5_file_list.txt'))
ALL_FILES = ALL_FILES + provider.getDataFiles(\
    os.path.join(BASE_DIR, 'part_seg/hdf5_data/val_hdf5_file_list.txt'))

print(ALL_FILES)

train_file_idxs = np.arange(0, len(TRAIN_FILES))
test_file_idxs = np.arange(0, len(TEST_FILES))
#val_file_idxs = np.arange(0, len(EVAL_FILES))
all_file_idxs = np.arange(0, len(ALL_FILES))

airplane_data=[]

#0: voxel, 1: category label 2: segmentation label
for i in range(len(ALL_FILES)):
    voxel,category,segmentation=provider.load_h5_data_label_seg(ALL_FILES[all_file_idxs[i]])
    #print(category)
    for j in range(len(category)):
        if category[j]==0:
            airplane_data=airplane_data+[[voxel[j],category[j],segmentation[j]]]
print(len(airplane_data))
sample = airplane_data[13]
#print(airplane_data[0])
print(sample[2])
part0=np.array([[0,0,0]])
part1=np.array([[0,0,0]])
part2=np.array([[0,0,0]])
part3=np.array([[0,0,0]])
for index in range(len(sample[0])):
    if sample[2][index]==0:
        add=(sample[0][index][0],sample[0][index][1],sample[0][index][2])
        part0=np.vstack((part0,add))
    if sample[2][index] == 1:
        add = (sample[0][index][0], sample[0][index][1], sample[0][index][2])
        part1 = np.vstack((part1, add))
    if sample[2][index] == 2:
        add = (sample[0][index][0], sample[0][index][1], sample[0][index][2])
        part2 = np.vstack((part2, add))
    if sample[2][index] == 3:
        add = (sample[0][index][0], sample[0][index][1], sample[0][index][2])
        part3 = np.vstack((part3, add))
#part0=part0[1:]; part1=part1[1:]; part2=part2[1:]; part3=part3[1:]
print(len(part0))
print(len(part1))
print(len(part2))
print(len(part3))
print(len(part0)+len(part1)+len(part2)+len(part3))
#X= [i[0] for i in part0]+[i[0] for i in part1]+[i[0] for i in part2]+[i[0] for i in part3]
#Y= [i[1] for i in part0]+[i[1] for i in part1]+[i[1] for i in part2]+[i[1] for i in part3]
#Z= [i[2] for i in part0]+[i[2] for i in part1]+[i[2] for i in part2]+[i[2] for i in part3]

X= [i[0] for i in part3]
Y= [i[1] for i in part3]
Z= [i[2] for i in part3]

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(X,Y,Z)
#plt.show()
"""