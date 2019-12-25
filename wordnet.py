from nltk.corpus import wordnet
import sys

def get_synset(word):
    syns = wordnet.synsets(word)
    syns_length = len(syns)
    print (syns_length)
    definitions = []
    count = 0
    for syn in syns:
        if (count > 4):
            break
        syn_dict = {}
        syn_dict['lexname'] = syn.lexname().split('.')[0][0] + "."
        syn_dict['definition'] = syn.definition()
        definitions.append(syn_dict)
        count = count + 1
    return definitions

#definitions = get_synset(word)
#print (definitions)