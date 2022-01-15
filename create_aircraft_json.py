import json
import math
import csv

json_data= open("airplane_result.json").read()
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


""""#making airplane_before_ontology.json file"""
result={}

""" Model Name, wordnet synset, wordnet lemma data"""
with open('/ssd2/Shapenet/ShapeNetCore.v1/02691156.csv', 'r') as raw:
    cooked = csv.reader(raw)
    idx=1
    for item in cooked:
        if item[0][4:] in data.keys():
            result[item[0][4:]]={"name" : item[5], "synset" : item[1].split(','), "lemma" :  item[2].split(',')}
            idx+=1


for i in range(len(data)):
#for i in range(5):
    model_id=data.items()[i][0]
    sample=data.items()[i][1]

    """Model size & numVertices"""
    normal_data = open("/ssd2/Shapenet/ShapeNetCore.v2/02691156/"+model_id+"/models/model_normalized.json").read()
    normal = json.loads(normal_data)
    result[model_id]["numVertices"]=normal["numVertices"]
    result[model_id]["size"]=[normal["max"][0]-normal["min"][0],normal["max"][1]-normal["min"][1],normal["max"][2]-normal["min"][2]]
    #size : [width, height, length]
    #another all size : [length, height, width]
    scale_factor = math.sqrt(result[model_id]["size"][0]**2+result[model_id]["size"][1]**2+result[model_id]["size"][2]**2)
    #part 1 : body
    body=[]
    #part 2 : wing
    wing=[]
    left_wing=[]
    right_wing=[]
    #part 3 : tail
    tail=[]
    #part 4 : engine
    engine=[]
    left_engine=[]
    right_engine=[]

    #devide parts
    for index in range(len(sample["seg_label"])):
        if sample["seg_label"][index]==1:
            body=body+[sample["points"][index]]
        if sample["seg_label"][index]==2:
            wing=wing+[sample["points"][index]]
        if sample["seg_label"][index]==3:
            tail=tail+[sample["points"][index]]
        if sample["seg_label"][index]==4:
            engine=engine+[sample["points"][index]]
    #right : +, left : -
    for index in range(len(wing)):
        if wing[index][2]<=0:
            left_wing=left_wing+[wing[index]]
        if wing[index][2]>=0:
            right_wing=right_wing+[wing[index]]
    for index in range(len(engine)):
        if engine[index][2]<=0:
            left_engine=left_engine+[engine[index]]
        if engine[index][2]>=0:
            right_engine=right_engine+[engine[index]]
    maxmin_body = []
    maxmin_leftwing = []
    maxmin_rightwing = []
    maxmin_tail = []
    maxmin_leftengine = []
    maxmin_rightengine=[]

    #extract max,min,avg for body
    max_x = -10
    min_x = 10
    max_y = -10
    min_y = 10
    max_z = -10
    min_z = 10
    sum_x=0
    sum_y=0
    sum_z=0
    for j in range(len(body)):
        sum_x+=body[j][0]
        sum_y += body[j][1]
        sum_z += body[j][2]
        if body[j][0] >= max_x:
            max_x = body[j][0]
        if body[j][1] >= max_y:
            max_y = body[j][1]
        if body[j][2] >= max_z:
            max_z = body[j][2]
        if body[j][0] <= min_x:
            min_x = body[j][0]
        if body[j][1] <= min_y:
            min_y = body[j][1]
        if body[j][2] <= min_z:
            min_z = body[j][2]
    maxmin_body = maxmin_body + [max_x, min_x, max_y, min_y, max_z, min_z]
    if(len(body)!=0):
        avg_body = [sum_x/len(body),sum_y/len(body),sum_z/len(body)]
    else:
        avg_body = -1

    # extract max,min,avg for wings
    max_x = -10
    min_x = 10
    max_y = -10
    min_y = 10
    max_z = -10
    min_z = 10
    sum_x=0
    sum_y=0
    sum_z=0
    for j in range(len(left_wing)):
        sum_x += left_wing[j][0]
        sum_y += left_wing[j][1]
        sum_z += left_wing[j][2]
        if left_wing[j][0] >= max_x:
            max_x = left_wing[j][0]
        if left_wing[j][1] >= max_y:
            max_y = left_wing[j][1]
        if left_wing[j][2] >= max_z:
            max_z = left_wing[j][2]
        if left_wing[j][0] <= min_x:
            min_x = left_wing[j][0]
        if left_wing[j][1] <= min_y:
            min_y = left_wing[j][1]
        if left_wing[j][2] <= min_z:
            min_z = left_wing[j][2]
    maxmin_leftwing = maxmin_leftwing + [max_x, min_x, max_y, min_y, max_z, min_z]
    if(len(left_wing)!=0):
        avg_leftwing = [sum_x/len(left_wing),sum_y/len(left_wing),sum_z/len(left_wing)]
    else:
        avg_leftwing = -1

    max_x = -10
    min_x = 10
    max_y = -10
    min_y = 10
    max_z = -10
    min_z = 10
    sum_x = 0
    sum_y = 0
    sum_z = 0
    for j in range(len(right_wing)):
        sum_x += right_wing[j][0]
        sum_y += right_wing[j][1]
        sum_z += right_wing[j][2]
        if right_wing[j][0] >= max_x:
            max_x = right_wing[j][0]
        if right_wing[j][1] >= max_y:
            max_y = right_wing[j][1]
        if right_wing[j][2] >= max_z:
            max_z = right_wing[j][2]
        if right_wing[j][0] <= min_x:
            min_x = right_wing[j][0]
        if right_wing[j][1] <= min_y:
            min_y = right_wing[j][1]
        if right_wing[j][2] <= min_z:
            min_z = right_wing[j][2]
    maxmin_rightwing = maxmin_rightwing + [max_x, min_x, max_y, min_y, max_z, min_z]
    if (len(right_wing) != 0):
        avg_rightwing = [sum_x / len(right_wing), sum_y / len(right_wing), sum_z / len(right_wing)]
    else:
        avg_rightwing = -1

    # extract max,min,avg for tail
    max_x = -10
    min_x = 10
    max_y = -10
    min_y = 10
    max_z = -10
    min_z = 10
    sum_x=0
    sum_y=0
    sum_z=0
    for j in range(len(tail)):
        sum_x += tail[j][0]
        sum_y += tail[j][1]
        sum_z += tail[j][2]
        if tail[j][0] >= max_x:
            max_x = tail[j][0]
        if tail[j][1] >= max_y:
            max_y = tail[j][1]
        if tail[j][2] >= max_z:
            max_z = tail[j][2]
        if tail[j][0] <= min_x:
            min_x = tail[j][0]
        if tail[j][1] <= min_y:
            min_y = tail[j][1]
        if tail[j][2] <= min_z:
            min_z = tail[j][2]
    maxmin_tail = maxmin_tail + [max_x, min_x, max_y, min_y, max_z, min_z]
    if(len(tail)!=0):
        avg_tail = [sum_x/len(tail),sum_y/len(tail),sum_z/len(tail)]
    else:
        avg_tail= -1

    # extract max,min,avg for engines
    max_x = -10
    min_x = 10
    max_y = -10
    min_y = 10
    max_z = -10
    min_z = 10
    sum_x=0
    sum_y=0
    sum_z=0
    for j in range(len(left_engine)):
        sum_x += left_engine[j][0]
        sum_y += left_engine[j][1]
        sum_z += left_engine[j][2]
        if left_engine[j][0] >= max_x:
            max_x = left_engine[j][0]
        if left_engine[j][1] >= max_y:
            max_y = left_engine[j][1]
        if left_engine[j][2] >= max_z:
            max_z = left_engine[j][2]
        if left_engine[j][0] <= min_x:
            min_x = left_engine[j][0]
        if left_engine[j][1] <= min_y:
            min_y = left_engine[j][1]
        if left_engine[j][2] <= min_z:
            min_z = left_engine[j][2]
    maxmin_leftengine = maxmin_leftengine + [max_x, min_x, max_y, min_y, max_z, min_z]
    if(len(left_engine)!=0):
        avg_leftengine = [sum_x/len(left_engine),sum_y/len(left_engine),sum_z/len(left_engine)]
    else:
        avg_leftengine = -1
    max_x = -10
    min_x = 10
    max_y = -10
    min_y = 10
    max_z = -10
    min_z = 10
    sum_x=0
    sum_y=0
    sum_z=0
    for j in range(len(right_engine)):
        sum_x += right_engine[j][0]
        sum_y += right_engine[j][1]
        sum_z += right_engine[j][2]
        if right_engine[j][0] >= max_x:
            max_x = right_engine[j][0]
        if right_engine[j][1] >= max_y:
            max_y = right_engine[j][1]
        if right_engine[j][2] >= max_z:
            max_z = right_engine[j][2]
        if right_engine[j][0] <= min_x:
            min_x = right_engine[j][0]
        if right_engine[j][1] <= min_y:
            min_y = right_engine[j][1]
        if right_engine[j][2] <= min_z:
            min_z = right_engine[j][2]
    maxmin_rightengine = maxmin_rightengine + [max_x, min_x, max_y, min_y, max_z, min_z]
    if(len(right_engine)!=0):
        avg_rightengine = [sum_x/len(right_engine),sum_y/len(right_engine),sum_z/len(right_engine)]
    else:
        avg_rightengine = -1
    if(body!=[]):
        size_body=[(maxmin_body[0]-maxmin_body[1])*scale_factor,(maxmin_body[2]-maxmin_body[3])*scale_factor,(maxmin_body[4]-maxmin_body[5])*scale_factor]
        location_body=[avg_body[0]*scale_factor,avg_body[1]*scale_factor,avg_body[2]*scale_factor]
    else:
        size_body=[0,0,0]
        location_body=[]

    if (left_wing != []):
        size_leftwing = [(maxmin_leftwing[0] - maxmin_leftwing[1]) * scale_factor, (maxmin_leftwing[2] - maxmin_leftwing[3]) * scale_factor, (maxmin_leftwing[4] - maxmin_leftwing[5]) * scale_factor]
        location_leftwing=[avg_leftwing[0]*scale_factor,avg_leftwing[1]*scale_factor,avg_leftwing[2]*scale_factor]
    else:
        size_leftwing = [0, 0, 0]
        location_leftwing=[]
    if (right_wing != []):
        size_rightwing = [(maxmin_rightwing[0] - maxmin_rightwing[1]) * scale_factor, (maxmin_rightwing[2] - maxmin_rightwing[3]) * scale_factor, (maxmin_rightwing[4] - maxmin_rightwing[5]) * scale_factor]
        location_rightwing=[avg_rightwing[0]*scale_factor,avg_rightwing[1]*scale_factor,avg_rightwing[2]*scale_factor]
    else:
        size_rightwing = [0, 0, 0]
        location_rightwing=[]

    if (tail != []):
        size_tail = [(maxmin_tail[0] - maxmin_tail[1]) * scale_factor, (maxmin_tail[2] - maxmin_tail[3]) * scale_factor,(maxmin_tail[4] - maxmin_tail[5]) * scale_factor]
        location_tail=[avg_tail[0]*scale_factor,avg_tail[1]*scale_factor,avg_tail[2]*scale_factor]
    else:
        size_tail = [0, 0, 0]
        location_tail=[]

    if (left_engine != []):
        size_leftengine = [(maxmin_leftengine[0] - maxmin_leftengine[1]) * scale_factor, (maxmin_leftengine[2] - maxmin_leftengine[3]) * scale_factor,(maxmin_leftengine[4] - maxmin_leftengine[5]) * scale_factor]
        location_leftengine=[avg_leftengine[0]*scale_factor,avg_leftengine[1]*scale_factor,avg_leftengine[2]*scale_factor]
    else:
        size_leftengine = [0, 0, 0]
        location_leftengine=[]
    if (right_engine != []):
        size_rightengine = [(maxmin_rightengine[0] - maxmin_rightengine[1]) * scale_factor, (maxmin_rightengine[2] - maxmin_rightengine[3]) * scale_factor,(maxmin_rightengine[4] - maxmin_rightengine[5]) * scale_factor]
        location_rightengine=[avg_rightengine[0]*scale_factor,avg_rightengine[1]*scale_factor,avg_rightengine[2]*scale_factor]
    else:
        size_rightengine = [0, 0, 0]
        location_rightengine=[]

    """part size and location"""
    #put in the dictionary
    result[model_id]["bodysize"] = size_body
    result[model_id]["wingsize"] = [(size_leftwing[0]+size_rightwing[0])/2,(size_leftwing[1]+size_rightwing[1])/2,(size_leftwing[2]+size_rightwing[2])/2]
    result[model_id]["tailsize"] = size_tail
    result[model_id]["enginesize"] = [(size_leftengine[0]+size_rightengine[0])/2,(size_leftengine[1]+size_rightengine[1])/2,(size_leftengine[2]+size_rightengine[2])/2]


    result[model_id]["bodylocation"] = location_body
    result[model_id]["leftwinglocation"] = location_leftwing
    result[model_id]["rightwinglocation"] = location_rightwing
    result[model_id]["taillocation"] = location_tail
    result[model_id]["leftenginelocation"] = location_leftengine
    result[model_id]["rightenginelocation"] = location_rightengine
    print(i)


with open('airplane_before_ontology.json', 'w') as fp:
    json.dump(result, fp)