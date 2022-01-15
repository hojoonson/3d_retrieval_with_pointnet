import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import provider

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
sample = airplane_data[152]
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
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X,Y,Z,s=2)
X= [i[0] for i in part2]
Y= [i[1] for i in part2]
Z= [i[2] for i in part2]
ax.scatter(X,Y,Z,s=2)
X= [i[0] for i in part1]
Y= [i[1] for i in part1]
Z= [i[2] for i in part1]
ax.scatter(X,Y,Z,s=2)
X= [i[0] for i in part0]
Y= [i[1] for i in part0]
Z= [i[2] for i in part0]
ax.scatter(X,Y,Z,s=2)

ax.set_xlim3d(-1,1)
ax.set_ylim3d(-1,1)
ax.set_zlim3d(-1,1)
plt.axis('off')
plt.show()