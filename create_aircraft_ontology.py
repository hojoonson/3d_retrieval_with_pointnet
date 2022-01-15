import json
import os
from owlready2 import get_ontology, OrderedDict, Thing

'''Python 3 code'''
json_data = open('airplane_before_ontology.json').read()
data = json.loads(json_data)
owl_path = os.path.join('/var','www', 'html', 'owl')
'''
dictionary form
name, synset, lemma, numVertices,
size,
bodysize, wingsize, tailsize, enginesize,
bodylocation, leftwinglocation, rightwinglocation, taillocation, leftenginelocation, rightenginelocation
'''
onto = get_ontology('airplane_1.owl')
onto.load()


#For python 3.5, make dictionary key list
data=OrderedDict(sorted(data.items()))
model_list=list(data.keys())
c1=0; c2=0; c3=0; c4=0; c5=0; c6=0; c7=0; c8=0; c9=0
state_null=0
for i in range(len(data)):
    model_id=model_list[i]
    sample=data[model_id]
    print(model_id,i+1)
    print(sample)
    onto.save(file=os.path.join(owl_path, f'{model_id}.owl'), format="rdfxml")
    onto = get_ontology(f'http://localhost:8080/owl/{model_id}.owl')

    ontology_state=''
    with onto:
        class Aircraft(Thing):
            pass
        class Name(Aircraft):
            range=[str]
        class Synset(Aircraft):
            range = [str]
        class Lemma(Synset):
            range = [str]
        class numVertices(Aircraft):
            range = [int]
        class Parts(Aircraft):
            pass
        class Body(Parts):
            pass
        
        class Size(Aircraft):
            pass
        class Height(Size):
            range=[float]
        class Width(Size):
            range=[float]
        class Length(Size):
            range=[float]

        class Location(Aircraft):
            pass
        class X_Location(Location):
            pass
        class Y_Location(Location):
            pass
        class Z_Location(Location):
            pass

        class Body(Location):
            pass
        class Body(Size):
            pass

        '''1 : tail exist, 2: tail & body are one'''
        if sample['taillocation']!=[]:
            class Tail(Body):
                pass
            if sample['leftwinglocation'] == [] and sample['leftenginelocation'] == []:
                ontology_state = 'body contains all_1'
                c1+=1
                pass
            if sample['leftwinglocation'] == [] and sample['leftenginelocation'] != []:
                c2 += 1
                ontology_state = 'body contains wing_1'
                class Engine(Body):
                    pass
                class LeftEngine(Engine):
                    pass
                class RightEngine(Engine):
                    pass
            if sample['leftwinglocation'] != [] and sample['leftenginelocation'] == []:
                c3 += 1
                ontology_state = 'body contains engine_1'
                class Wing(Body):
                    pass
                class LeftWing(Wing):
                    pass
                class RightWing(Wing):
                    pass

            if sample['leftenginelocation']!=[] and sample['leftwinglocation']!=[]:
                if abs(sample['leftwinglocation'][0]-sample['leftenginelocation'][0]) <= abs(sample['taillocation'][0]-sample['leftenginelocation'][0]):
                    ontology_state='engine at wing_1'
                    c4+=1
                    class Wing(Body):
                        pass
                    class LeftWing(Wing):
                        pass
                    class RightWing(Wing):
                        pass

                    class Engine(Wing):
                        pass
                    class LeftEngine(Engine):
                        pass
                    class RightEngine(Engine):
                        pass

                    class Tail(Location):
                        pass
                    class Tail(Size):
                        pass
                    class Wing(Location):
                        pass
                    class Wing(Size):
                        pass
                    class Engine(Location):
                        pass
                    class Engine(Size):
                        pass
                else:
                    ontology_state='engine at body_1'
                    c5+=1
                    class Wing(Body):
                        pass
                    class Wing(Body):
                        pass
                    class LeftWing(Wing):
                        pass
                    class RightWing(Wing):
                        pass

                    class Engine(Body):
                        pass
                    class LeftEngine(Engine):
                        pass
                    class RightEngine(Engine):
                        pass
                    
        else:
            if sample['leftwinglocation'] == [] and sample['leftenginelocation'] == []:
                ontology_state = 'body contains all_2'
                c6+=1
                pass
            if sample['leftwinglocation'] == [] and sample['leftenginelocation'] != []:
                c7 += 1
                ontology_state = 'body contains wing_2'
                class Engine(Body):
                    pass
                class LeftEngine(Engine):
                    pass
                class RightEngine(Engine):
                    pass
            if sample['leftwinglocation'] != [] and sample['leftenginelocation'] == []:
                c8 += 1
                ontology_state = 'body contains engine_2'
                class Wing(Body):
                    pass
                class LeftWing(Wing):
                    pass
                class RightWing(Wing):
                    pass
            if sample['leftenginelocation']!=[] and sample['leftwinglocation']!=[]:
                    ontology_state='engine at wing_2'
                    c9+=1
                    class Wing(Body):
                        pass
                    class LeftWing(Wing):
                        pass
                    class RightWing(Wing):
                        pass
                    class Engine(Wing):
                        pass
                    class LeftEngine(Engine):
                        pass
                    class RightEngine(Engine):
                        pass
    if ontology_state=='':
        state_null+=1
    onto.save(file=os.path.join(owl_path, f'{model_id}.owl'), format="rdfxml")
print(c1,c2,c3,c4,c5,c6,c7,c8,c9)
print(state_null)