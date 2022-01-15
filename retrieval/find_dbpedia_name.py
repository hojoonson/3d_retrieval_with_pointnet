import json
import csv
import math
from sematch.semantic.similarity import EntitySimilarity
from sematch.semantic.similarity import WordNetSimilarity

##Python 2.7 code
json_data = open("../airplane_before_ontology.json").read()
data = json.loads(json_data)

f = open('./Name.csv','w+')
csvWriter = csv.writer(f)
csvWriter.writerow(['model','name'])

for i in range(len(data)):
    try:
        print(data.items()[i][0])
        print(data.items()[i][1]['name'])
        csvWriter.writerow([data.items()[i][0],data.items()[i][1]['name']])
    except:
        pass
f.close()