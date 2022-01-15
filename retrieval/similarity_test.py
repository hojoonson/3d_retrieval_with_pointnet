from sematch.semantic.similarity import EntitySimilarity

entity_sim = EntitySimilarity()


from sematch.semantic.similarity import WordNetSimilarity
wns = WordNetSimilarity()

from sematch.semantic.graph import DBpediaDataTransform, Taxonomy
from sematch.semantic.similarity import ConceptSimilarity
concept = ConceptSimilarity(Taxonomy(DBpediaDataTransform()),'models/dbpedia_type_ic.txt')

print entity_sim.relatedness("http://dbpedia.org/resource/Boeing_747" , "http://dbpedia.org/resource/Airplane")
print entity_sim.similarity("http://dbpedia.org/resource/Aircraft" , "http://dbpedia.org/resource/Aircraft")
print entity_sim.similarity('http://dbpedia.org/resource/Madrid','http://dbpedia.org/resource/Barcelona')
"""
print wns.word_similarity('dog','cat','li')
print wns.word_similarity('dog','cat','lin')
print wns.word_similarity('dog','cat','wup')
print wns.word_similarity('dog','cat','res')
print wns.word_similarity('dog','cat','jcn')
print wns.word_similarity('dog','cat','wpath')

print (wns.word_similarity('dog','cat','li')+wns.word_similarity('dog','cat','lin'))/2
print wns.word_similarity('dog','cat')

print wns.word_similarity('airplane','jet')
print wns.word_similarity('jet','fighter')
print wns.word_similarity('airplane','fighter')
"""
