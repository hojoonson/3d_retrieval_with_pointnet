import json
import math
import csv
from fractions import Fraction
from sematch.semantic.similarity import EntitySimilarity
from sematch.semantic.similarity import WordNetSimilarity
entity_sim = EntitySimilarity()
wns = WordNetSimilarity()

##Python 2.7 code
json_data = open("../airplane_before_ontology.json").read()
data = json.loads(json_data)
"""
dictionary form
name, synset, lemma, numVertices,
size,
bodysize, wingsize, tailsize, enginesize,
bodylocation, leftwinglocation, rightwinglocation, taillocation, leftenginelocation, rightenginelocation
dbpedia
"""
#size : [width, height, length]
#another all size : [length, height, width]
#location : [x,z,y]

samplelist={}
f = open('Name_all.csv', 'r')
rdr = csv.reader(f)
for line in rdr:
#    if(line[2]!='' and line[0]!='model'):
    if(line[0]!='model'):
        print(line)
        data[line[0]]['dbpedia']=line[2]
        samplelist[line[0]]=data[line[0]]
print(len(samplelist))

testlist={'1f08b579e153b2de313f9af5275b7c70' : data['1f08b579e153b2de313f9af5275b7c70']
            ,'9d7e431ebd35cdc2bd46d022fd7d80aa' : data['9d7e431ebd35cdc2bd46d022fd7d80aa']
            ,'bb785567f73903da2661ac6da30aefd' : data['bb785567f73903da2661ac6da30aefd']
            ,'5fc63354b0156d113136bac5fdb5050a' : data['5fc63354b0156d113136bac5fdb5050a']
            ,'2c64c521c114df40e51f766854841067' : data['2c64c521c114df40e51f766854841067']
            ,'1af4b32eafffb0f7ee60c37cbf99c1c' : data['1af4b32eafffb0f7ee60c37cbf99c1c']}

#print(len(samplelist))
#5f
#1f
#1af


def cosin_sim (v1, v2):
    size1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2 + v1[2] ** 2)
    size2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2 + v2[2] ** 2)
    inner_pro=v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]
    similarity = inner_pro/(size1*size2)
    return similarity


state_null=0
c1 = 0;c2 = 0;c3 = 0;c4 = 0;c5 = 0;c6 = 0;c7 = 0;c8 = 0;c9 = 0

for i in range(len(testlist)):
    model_id=testlist.items()[i][0]
    sample=testlist.items()[i][1]
    print("\n"+model_id + "    "+sample['dbpedia'])

    f = open("3D Retrieval Result_pointnet_mod.txt", 'a+')
    data = model_id + "    "+sample['dbpedia'] + "\n"
    f.write(data)


    similarity_all=0
    mostsim_model_all=[]
    """1 : tail exist, 2: tail & body are one"""
    if sample["taillocation"] != []:
        if sample["leftwinglocation"] == [] and sample["leftenginelocation"] == []:
            ontology_state = "1"
            c1 += 1
        if sample["leftwinglocation"] == [] and sample["leftenginelocation"] != []:
            c2 += 1
            ontology_state = "2"

        if sample["leftwinglocation"] != [] and sample["leftenginelocation"] == []:
            c3 += 1
            ontology_state = "3"

        if sample["leftenginelocation"] != [] and sample["leftwinglocation"] != []:
            if abs(sample["leftwinglocation"][0] - sample["leftenginelocation"][0]) <= abs(sample["taillocation"][0] - sample["leftenginelocation"][0]):
                ontology_state = "4"
                c4 += 1
            else:
                ontology_state = "5"
                c5 += 1
    else:
        if sample["leftwinglocation"] == [] and sample["leftenginelocation"] == []:
            ontology_state = "out"
            c6 += 1
        if sample["leftwinglocation"] == [] and sample["leftenginelocation"] != []:
            ontology_state="out"
            c7 += 1
        if sample["leftwinglocation"] != [] and sample["leftenginelocation"] == []:
            ontology_state = "6"
            c8 += 1
        if sample["leftenginelocation"] != [] and sample["leftwinglocation"] != []:
            ontology_state = "7"
            c9 += 1
    print(ontology_state)
    d1 = 0;d2 = 0;d3 = 0;d4 = 0;d5 = 0;d6 = 0;d7 = 0;d8 = 0;d9 = 0
    for j in range(len(samplelist)):
        model_id_c = samplelist.items()[j][0]
        sample_c = samplelist.items()[j][1]

        if model_id !=model_id_c:
            if sample_c["taillocation"] != []:
                if sample_c["leftwinglocation"] == [] and sample_c["leftenginelocation"] == []:
                    ontology_state_c = "1"
                    d1 += 1
                if sample_c["leftwinglocation"] == [] and sample_c["leftenginelocation"] != []:
                    d2 += 1
                    ontology_state_c = "2"

                if sample_c["leftwinglocation"] != [] and sample_c["leftenginelocation"] == []:
                    d3 += 1
                    ontology_state_c = "3"

                if sample_c["leftenginelocation"] != [] and sample_c["leftwinglocation"] != []:
                    if abs(sample_c["leftwinglocation"][0] - sample_c["leftenginelocation"][0]) <= abs(sample_c["taillocation"][0] - sample_c["leftenginelocation"][0]):
                        ontology_state_c = "4"
                        d4 += 1
                    else:
                        ontology_state_c = "5"
                        d5 += 1
            else:
                if sample_c["leftwinglocation"] == [] and sample_c["leftenginelocation"] == []:
                    ontology_state_c = "out"
                    d6 += 1
                if sample_c["leftwinglocation"] == [] and sample_c["leftenginelocation"] != []:
                    ontology_state_c="out"
                    d7 += 1
                if sample_c["leftwinglocation"] != [] and sample_c["leftenginelocation"] == []:
                    ontology_state_c = "6"
                    d8 += 1
                if sample_c["leftenginelocation"] != [] and sample_c["leftwinglocation"] != []:
                    ontology_state_c = "7"
                    d9 += 1
            print("\n"+ontology_state_c)
            print("iteration : " + str(j))
            #Semantic Similarity Wing, Engine, Tail
            semanticsim=0
            if (ontology_state=="1" and ontology_state_c=="2") or (ontology_state=="2" and ontology_state_c=="1"):
                semanticsim=(1+2.0/3+1)/3
            if (ontology_state=="1" and ontology_state_c=="3") or (ontology_state=="3" and ontology_state_c=="1"):
                semanticsim=(2.0/3+1+1)/3
            if (ontology_state=="1" and ontology_state_c=="4") or (ontology_state=="4" and ontology_state_c=="1"):
                semanticsim=(2.0/3+1.0/2+1)/3
            if (ontology_state=="1" and ontology_state_c=="5") or (ontology_state=="5" and ontology_state_c=="1"):
                semanticsim=(2.0/3+2.0/3+1)/3
            if (ontology_state=="1" and ontology_state_c=="6") or (ontology_state=="6" and ontology_state_c=="1"):
                semanticsim=(2.0/3+1+2.0/3)/3
            if (ontology_state=="1" and ontology_state_c=="7") or (ontology_state=="7" and ontology_state_c=="1"):
                semanticsim=(2.0/3+1.0/2+2.0/3)/3
            if (ontology_state=="2" and ontology_state_c=="3") or (ontology_state=="3" and ontology_state_c=="2"):
                semanticsim=(2.0/3+2.0/3+1)/3
            if (ontology_state=="2" and ontology_state_c=="4") or (ontology_state=="4" and ontology_state_c=="2"):
                semanticsim=(2.0/3+2.0/5+1)/3
            if (ontology_state=="2" and ontology_state_c=="5") or (ontology_state=="5" and ontology_state_c=="2"):
                semanticsim=(2.0/3+1+1)/3
            if (ontology_state=="2" and ontology_state_c=="6") or (ontology_state=="6" and ontology_state_c=="2"):
                semanticsim=(2.0/3+2.0/3+2.0/3)/3
            if (ontology_state=="2" and ontology_state_c=="7") or (ontology_state=="7" and ontology_state_c=="2"):
                semanticsim=(2.0/3+2.0/5+2.0/3)/3
            if (ontology_state=="3" and ontology_state_c=="4") or (ontology_state=="4" and ontology_state_c=="3"):
                semanticsim=(1+1.0/2+1)/3
            if (ontology_state=="3" and ontology_state_c=="5") or (ontology_state=="5" and ontology_state_c=="3"):
                semanticsim=(1+2.0/3+1)/3
            if (ontology_state=="3" and ontology_state_c=="6") or (ontology_state=="6" and ontology_state_c=="3"):
                semanticsim=(1+1+2.0/3)/3
            if (ontology_state=="3" and ontology_state_c=="7") or (ontology_state=="7" and ontology_state_c=="3"):
                semanticsim=(1+1.0/2+2.0/3)/3
            if (ontology_state=="4" and ontology_state_c=="5") or (ontology_state=="5" and ontology_state_c=="4"):
                semanticsim=(1+2.0/5+1)/3
            if (ontology_state=="4" and ontology_state_c=="6") or (ontology_state=="6" and ontology_state_c=="4"):
                semanticsim=(1+2.0/3+1.0/2)/3
            if (ontology_state=="4" and ontology_state_c=="7") or (ontology_state=="7" and ontology_state_c=="4"):
                semanticsim=(1+1+2.0/3)/3
            if (ontology_state=="5" and ontology_state_c=="6") or (ontology_state=="6" and ontology_state_c=="5"):
                semanticsim=(1+2.0/3+2.0/3)/3
            if (ontology_state=="5" and ontology_state_c=="7") or (ontology_state=="7" and ontology_state_c=="5"):
                semanticsim=(1+2.0/5+2.0/3)/3
            if (ontology_state=="6" and ontology_state_c=="7") or (ontology_state=="7" and ontology_state_c=="6"):
                semanticsim=(1+1.0/2+1)/3
            if ontology_state==ontology_state_c:
                semanticsim=1
            #print((1+2.0/3+1)/3.0)
            print("semantic similarity : " + str(semanticsim))
            # data = "semantic similarity : " + str(semanticsim)+"\n"
            # f.write(data)


            #bodylocation, leftwinglocation, rightwinglocation, taillocation, leftenginelocation, rightenginelocation
            #Location Similarity Calculation
            locationsim=0
            count=0
            if sample['bodylocation']!=[]:
                try:
                    v1=sample['bodylocation']
                    v2=sample_c['bodylocation']
                    locationsim+=cosin_sim(v1,v2)
                    count+=1
                except:
                    count+=1
                    pass
            else:
                if sample_c['bodylocation']!=[]:
                    count+=1

            if sample['leftwinglocation'] != []:
                try:
                    v1=sample['leftwinglocation']
                    v2=sample_c['leftwinglocation']
                    locationsim+=cosin_sim(v1,v2)
                    count+=1
                except:
                    count+=1
                    pass
            else:
                if sample_c['leftwinglocation']!=[]:
                    count+=1

            if sample['rightwinglocation'] !=[]:
                try:
                    v1=sample['rightwinglocation']
                    v2=sample_c['rightwinglocation']
                    locationsim+=cosin_sim(v1,v2)
                    count+=1
                except:
                    count += 1
                    pass
            else:
                if sample_c['rightwinglocation']!=[]:
                    count+=1

            if sample['taillocation']!=[] :
                try:
                    v1=sample['taillocation']
                    v2=sample_c['taillocation']
                    locationsim+=cosin_sim(v1,v2)
                    count+=1
                except:
                    count += 1
                    pass
            else:
                if sample_c['taillocation']!=[]:
                    count+=1

            if sample['leftenginelocation']!=[]:
                try:
                    v1=sample['leftenginelocation']
                    v2=sample_c['leftenginelocation']
                    locationsim+=cosin_sim(v1,v2)
                    count+=1
                except:
                    count += 1
                    pass
            else:
                if sample_c['leftenginelocation']!=[]:
                    count+=1

            if sample['rightenginelocation']!=[]:
                try:
                    v1=sample['rightenginelocation']
                    v2=sample_c['rightenginelocation']
                    locationsim+=cosin_sim(v1,v2)
                    count+=1
                except:
                    count += 1
                    pass
            else:
                if sample_c['rightenginelocation']!=[]:
                    count+=1
            locationsim=locationsim/count
            print("location similarity : " + str(locationsim))
            #data = "location similarity : " + str(locationsim)+"\n"
            #f.write(data)

            #Size Similarity
            #size,bodysize, wingsize, tailsize, enginesize,
            sizesim = 0
            count = 0
            if sample['size']!=[]:
                try:
                    v1=sample['size']
                    v2=sample_c['size']
                    sizesim+=cosin_sim(v1,v2)
                    count+=1
                except:
                    count += 1
                    pass
            else:
                if sample_c['size']!=[]:
                    count+=1

            if sample['bodysize']!=[]:
                try:
                    v1=sample['bodysize']
                    v2=sample_c['bodysize']
                    sizesim+=cosin_sim(v1,v2)
                    count+=1
                except:
                    count += 1
                    pass
            else:
                if sample_c['bodysize']!=[]:
                    count+=1

            if sample['wingsize']!=[]:
                try:
                    v1=sample['wingsize']
                    v2=sample_c['wingsize']
                    sizesim+=cosin_sim(v1,v2)
                    count+=1
                except:
                    count += 1
                    pass
            else:
                if sample_c['wingsize']!=[]:
                    count+=1

            if sample['tailsize']!=[]:
                try:
                    v1=sample['tailsize']
                    v2=sample_c['tailsize']
                    sizesim+=cosin_sim(v1,v2)
                    count+=1
                except:
                    count += 1
                    pass
            else:
                if sample_c['tailsize']!=[]:
                    count+=1

            if sample['enginesize']!=[]:
                try:
                    v1=sample['enginesize']
                    v2=sample_c['enginesize']
                    sizesim+=cosin_sim(v1,v2)
                    count+=1
                except:
                    count += 1
                    pass
            else:
                if sample_c['enginesize']!=[]:
                    count+=1

            sizesim = sizesim / count
            print("size similarity : " + str(sizesim))
            #data = "size similarity : " + str(sizesim)+"\n"
            #f.write(data)

            total_lemmasim=0
            for i1 in range(len(sample['lemma'])):
                for j1 in range(len(sample_c['lemma'])):
                    #print(wns.word_similarity(sample['lemma'][i1],sample_c['lemma'][j1]))
                    total_lemmasim+=wns.word_similarity(sample['lemma'][i1],sample_c['lemma'][j1])
            #print((i1+1)*(j1+1))
            #print("total : "+str(total_lemmasim))
            print("lemma similarity : "+str(total_lemmasim/((i1+1)*(j1+1))))
            #data = "lemma similarity : "+str(total_lemmasim/((i1+1)*(j1+1)))+"\n"
            #f.write(data)
            lemmasim=total_lemmasim/((i1+1)*(j1+1))
            
            
            namesim=0            
            namesim_ok=0
            while(namesim_ok==0):
                try:
                    if sample_c['dbpedia']==sample['dbpedia']:
                        namesim=-5
                        print("name similarity : samemodel")
                        totalsim=(lemmasim+locationsim+sizesim+semanticsim+namesim)/5
                        break
                    if  entity_sim.similarity('http://dbpedia.org/resource/'+sample_c['dbpedia'],'http://dbpedia.org/resource/'+sample_c['dbpedia'])!=0 :
                        if entity_sim.similarity('http://dbpedia.org/resource/'+sample['dbpedia'],'http://dbpedia.org/resource/'+sample['dbpedia'])!=0:
                            namesim=entity_sim.similarity('http://dbpedia.org/resource/'+sample['dbpedia'],'http://dbpedia.org/resource/'+sample_c['dbpedia'])
                            print("name similarity : " +str(namesim))
                            totalsim=(lemmasim+namesim+locationsim+sizesim+semanticsim)/5
                            #totalsim = (lemmasim + namesim) / 2
                            #data = "name similarity : " +str(entity_sim.similarity('http://dbpedia.org/resource/'+sample['dbpedia'],'http://dbpedia.org/resource/'+sample_c['dbpedia']))+"\n"
                            #f.write(data)
                            namesim_ok=1
                        else :
                            totalsim=(lemmasim+locationsim+sizesim+semanticsim)/4
                            #totalsim=lemmasim
                            namesim_ok=1

                    else:
                        namesim=0
                        #print("No name in DBpedia, Pass test model " + model_id_c)
                        print("name similarity : 0")
                        totalsim=(lemmasim+locationsim+sizesim+semanticsim)/4
                        #totalsim=(lemmasim+namesim)/2
                        #data = "No name in DBpedia, Pass test model " + model_id_c+"\n\n"
                        #f.write(data)
                        namesim_ok=1
                        pass
                except:
                    pass
            

            

            #totalsim=(locationsim+sizesim+semanticsim)/3
            #print("total similarity : "+str(totalsim))
            


            #data = "total similarity : "+str(totalsim)+"\n\n"
            #f.write(data)
            valid = 0
            if totalsim>similarity_all:
                similarity_all=totalsim
                #rank the similarity value in list mostsim_model ([-1] is most similar one)
                mostsim_model_all=mostsim_model_all+[[model_id_c,totalsim,lemmasim,locationsim,sizesim,semanticsim,namesim]]
                valid=1
                if len(mostsim_model_all)>=51:
                    mostsim_model_all.pop(0)
            else:
                if len(mostsim_model_all)<50:
                    for index in range(len(mostsim_model_all)):
                        print(mostsim_model_all[-1-index][1],totalsim)
                        if mostsim_model_all[-1-index][1]<=totalsim:
                            backup=mostsim_model_all[:-index]
                            mostsim_model_all[-1-index]=[model_id_c,totalsim,lemmasim,locationsim,sizesim,semanticsim,namesim]
                            for count in range(len(backup)-1):
                                mostsim_model_all.pop(0)
                            for count in range(len(backup)):
                                mostsim_model_all.insert(count,backup[count])
                            valid=1
                            break
                else:
                    for index in range(50):
                        if len(mostsim_model_all)==50:
                            if mostsim_model_all[-1-index][1]<=totalsim:
                                backup = mostsim_model_all[:-index]
                                mostsim_model_all[-1 - index] = [model_id_c, totalsim,lemmasim,locationsim,sizesim,semanticsim,namesim]
                                for count in range(len(backup) - 1):
                                    mostsim_model_all.pop(0)
                                for count in range(len(backup)):
                                    mostsim_model_all.insert(count, backup[count])
                                valid = 1
                                break
            if valid==0:
                mostsim_model_all.insert(0,[model_id_c,totalsim,lemmasim,locationsim,sizesim,semanticsim,namesim])
            if len(mostsim_model_all)>=51:
                mostsim_model_all.pop(0)

            for index in range(len(mostsim_model_all)):
                print(mostsim_model_all[index])
            print(len(mostsim_model_all))
    try:
        print("\nMost Similar Model :" + mostsim_model_all[-1][0])
        print("Similarity : " + str(mostsim_model_all[-1][1]))
        data=""
        for count in range(len(mostsim_model_all)):
            data = data+ "Most Similar Model"+ str(count+1)+":" + mostsim_model_all[-count-1][0] + "   " +"Total similarity : " + str(mostsim_model_all[-count-1][1])+ "   lemmasim : " + str(mostsim_model_all[-count-1][2])+ "   locationsim : " + str(mostsim_model_all[-count-1][3])+ "   sizesim : " + str(mostsim_model_all[-count-1][4])+ "   semanticsim(partalign) : " + str(mostsim_model_all[-count-1][5])+ "   namesim : " + str(mostsim_model_all[-count-1][6])+ "\n"
        f.write(data)
    except:
        print("There is no most similar model")
        data = "There is no most similar model"+"\n"
        f.write(data)
    f.write("\n\n")
    f.close()
    print("Targeted model ontology type counting : "+str((d1, d2, d3, d4, d5, d6, d7, d8, d9)))

print("Query model ontology type counting : " + str((c1, c2, c3, c4, c5, c6, c7, c8, c9)))

