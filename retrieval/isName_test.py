import json
import csv
from sematch.semantic.similarity import EntitySimilarity
entity_sim = EntitySimilarity()


json_data = open("../airplane_before_ontology.json").read()
data = json.loads(json_data)

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

index=0
count=1
for element in samplelist:
    if entity_sim.similarity('http://dbpedia.org/resource/'+samplelist[element]['dbpedia'],'http://dbpedia.org/resource/'+samplelist[element]['dbpedia'])!=1:
        print(element, samplelist[element]['dbpedia'])
        print("INDEX : "+str(index) + ", Count : "+str(count))
        count+=1
    index+=1