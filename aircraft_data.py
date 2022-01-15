import json
import math
import json
import csv



json_data = open("airplane_result.json").read()
data = json.loads(json_data)

# dictionary form :
# itemid : {"seg_label" , "points" , "max_x" , "min_x","max_y" ,"min_y" ,"max_z" ,"min_z" ,"local_max", "local_min"}

#sample=data["1a04e3eab45ca15dd86060f189eb133"]
#print(sample)
"""
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


""""making airplane_before_ontology.json file"""
result={}

""" Model Name, wordnet synset, wordnet lemma data"""
with open('/ssd2/Shapenet/ShapeNetCore.v1/02691156.csv', 'r') as raw:
    cooked = csv.reader(raw)
    idx=1
    for item in cooked:
        if item[0][4:] in data.keys():
            #print(idx,item[0][4:], item[1].split(','), item[2].split(','), item[5])
            result[item[0][4:]]={"name" : item[5], "synset" : item[1].split(','), "lemma" :  item[2].split(',')}
            #result[item[0][4:]]["test"]="test"
            #print(result[item[0][4:]],idx)
            idx+=1


for i in range(len(data)):
    model_id=data.items()[i][0]
    sample=data.items()[i][1]

    """Model size & numVertices"""
    normal_data = open("/ssd2/Shapenet/ShapeNetCore.v2/02691156/"+model_id+"/models/model_normalized.json").read()
    normal = json.loads(normal_data)
    #print(model_id)
    #print(normal)
    result[model_id]["numVertices"]=normal["numVertices"]
    result[model_id]["size"]=[normal["max"][0]-normal["min"][0],normal["max"][1]-normal["min"][1],normal["max"][2]-normal["min"][2]]

    scale_factor = math.sqrt(result[model_id]["size"][0]**2+result[model_id]["size"][1]**2+result[model_id]["size"][2]**2)
    #print(scale_factor)
    #print(result[model_id])
    #part 1 : body
    part1=[]
    #part 2 : wing
    part2=[]
    #part 3 : tail
    part3=[]
    #part 4 : engine
    part4=[]
    #devide parts
    for index in range(len(sample["seg_label"])):
        if sample["seg_label"][index]==1:
            part1=part1+[sample["points"][index]]
        if sample["seg_label"][index]==2:
            part2=part2+[sample["points"][index]]
        if sample["seg_label"][index]==3:
            part3=part3+[sample["points"][index]]
        if sample["seg_label"][index]==4:
            part4=part4+[sample["points"][index]]

    maxmin1 = []
    maxmin2 = []
    maxmin3 = []
    maxmin4 = []

    #print(sample["local_max"],sample["local_min"])
    #extract max,min,avg for part1
    max_x = -10
    min_x = 10
    max_y = -10
    min_y = 10
    max_z = -10
    min_z = 10
    sum_x=0
    sum_y=0
    sum_z=0
    for j in range(len(part1)):
        sum_x+=part1[j][0]
        sum_y += part1[j][1]
        sum_z += part1[j][2]
        if part1[j][0] >= max_x:
            max_x = part1[j][0]
        if part1[j][1] >= max_y:
            max_y = part1[j][1]
        if part1[j][2] >= max_z:
            max_z = part1[j][2]
        if part1[j][0] <= min_x:
            min_x = part1[j][0]
        if part1[j][1] <= min_y:
            min_y = part1[j][1]
        if part1[j][2] <= min_z:
            min_z = part1[j][2]
    maxmin1 = maxmin1 + [max_x, min_x, max_y, min_y, max_z, min_z]
    if(len(part1)!=0):
        avg1 = [sum_x/len(part1),sum_y/len(part1),sum_z/len(part1)]
    else:
        avg1 = -1
    # extract max,min,avg for part2
    max_x = -10
    min_x = 10
    max_y = -10
    min_y = 10
    max_z = -10
    min_z = 10
    sum_x=0
    sum_y=0
    sum_z=0
    for j in range(len(part2)):
        sum_x += part2[j][0]
        sum_y += part2[j][1]
        sum_z += part2[j][2]
        if part2[j][0] >= max_x:
            max_x = part2[j][0]
        if part2[j][1] >= max_y:
            max_y = part2[j][1]
        if part2[j][2] >= max_z:
            max_z = part2[j][2]
        if part2[j][0] <= min_x:
            min_x = part2[j][0]
        if part2[j][1] <= min_y:
            min_y = part2[j][1]
        if part2[j][2] <= min_z:
            min_z = part2[j][2]
    maxmin2 = maxmin2 + [max_x, min_x, max_y, min_y, max_z, min_z]
    if(len(part2)!=0):
        avg2 = [sum_x/len(part2),sum_y/len(part2),sum_z/len(part2)]
    else:
        avg2 = -1
    # extract max,min,avg for part3
    max_x = -10
    min_x = 10
    max_y = -10
    min_y = 10
    max_z = -10
    min_z = 10
    sum_x=0
    sum_y=0
    sum_z=0
    for j in range(len(part3)):
        sum_x += part3[j][0]
        sum_y += part3[j][1]
        sum_z += part3[j][2]
        if part3[j][0] >= max_x:
            max_x = part3[j][0]
        if part3[j][1] >= max_y:
            max_y = part3[j][1]
        if part3[j][2] >= max_z:
            max_z = part3[j][2]
        if part3[j][0] <= min_x:
            min_x = part3[j][0]
        if part3[j][1] <= min_y:
            min_y = part3[j][1]
        if part3[j][2] <= min_z:
            min_z = part3[j][2]
    maxmin3 = maxmin3 + [max_x, min_x, max_y, min_y, max_z, min_z]
    if(len(part3)!=0):
        avg3 = [sum_x/len(part3),sum_y/len(part3),sum_z/len(part3)]
    else:
        avg3 = -1
    # extract max,min,avg for part4
    max_x = -10
    min_x = 10
    max_y = -10
    min_y = 10
    max_z = -10
    min_z = 10
    sum_x=0
    sum_y=0
    sum_z=0
    for j in range(len(part4)):
        sum_x += part4[j][0]
        sum_y += part4[j][1]
        sum_z += part4[j][2]
        if part4[j][0] >= max_x:
            max_x = part4[j][0]
        if part4[j][1] >= max_y:
            max_y = part4[j][1]
        if part4[j][2] >= max_z:
            max_z = part4[j][2]
        if part4[j][0] <= min_x:
            min_x = part4[j][0]
        if part4[j][1] <= min_y:
            min_y = part4[j][1]
        if part4[j][2] <= min_z:
            min_z = part4[j][2]
    maxmin4 = maxmin4 + [max_x, min_x, max_y, min_y, max_z, min_z]
    if(len(part4)!=0):
        avg4 = [sum_x/len(part4),sum_y/len(part4),sum_z/len(part4)]
    else:
        avg4 = -1
    #print(maxmin1)
    #print(maxmin2)
    #print(maxmin3)
    #print(maxmin4)
    #print(avg1,avg2,avg3,avg4)
    if(part1!=[]):
        size1=[(maxmin1[0]-maxmin1[1])*scale_factor,(maxmin1[2]-maxmin1[3])*scale_factor,(maxmin1[4]-maxmin1[5])*scale_factor]
        location1=[avg1[0]*scale_factor,avg1[1]*scale_factor,avg1[2]*scale_factor]
    else:
        size1=[0,0,0]
        location1=[]
    if (part2 != []):
        size2 = [(maxmin2[0] - maxmin2[1]) * scale_factor, (maxmin2[2] - maxmin2[3]) * scale_factor, (maxmin2[4] - maxmin2[5]) * scale_factor]
        location2=[avg2[0]*scale_factor,avg2[1]*scale_factor,avg2[2]*scale_factor]
    else:
        size2 = [0, 0, 0]
        location2=[]
    if (part3 != []):
        size3 = [(maxmin3[0] - maxmin3[1]) * scale_factor, (maxmin3[2] - maxmin3[3]) * scale_factor,(maxmin3[4] - maxmin3[5]) * scale_factor]
        location3=[avg3[0]*scale_factor,avg3[1]*scale_factor,avg3[2]*scale_factor]
    else:
        size3 = [0, 0, 0]
        location3=[]
    if (part4 != []):
        size4 = [(maxmin4[0] - maxmin4[1]) * scale_factor, (maxmin4[2] - maxmin4[3]) * scale_factor,(maxmin4[4] - maxmin4[5]) * scale_factor]
        location4=[avg4[0]*scale_factor,avg4[1]*scale_factor,avg4[2]*scale_factor]
    else:
        size4 = [0, 0, 0]
        location4=[]
    #print(size1)
    #print(size2)
    #print(size3)
    #print(size4)
    #print(location1,location2,location3,location4)

    """part size and location"""
    #put in the dictionary
    result[model_id]["bodysize"] = size1
    result[model_id]["wingsize"] = size2
    result[model_id]["tailsize"] = size3
    result[model_id]["enginesize"] = size4

    result[model_id]["bodylocation"] = location1
    result[model_id]["winglocation"] = location2
    result[model_id]["taillocation"] = location3
    result[model_id]["enginelocation"] = location4

    #print(result[model_id])
    print(i)


with open('airplane_before_ontology.json', 'w') as fp:
    json.dump(result, fp)

    """
    try:
        X = [i[0] for i in part4]
        Y = [i[1] for i in part4]
        Z = [i[2] for i in part4]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(X, Y, Z)
        ax.set_xlim3d(sample["local_min"] - 0.1, sample["local_max"] + 0.1)
        ax.set_ylim3d(sample["local_min"] - 0.1, sample["local_max"] + 0.1)
        ax.set_zlim3d(sample["local_min"] - 0.1, sample["local_max"] + 0.1)
        plt.show()
    except:
        pass
    """