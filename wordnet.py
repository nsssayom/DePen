from nltk.corpus import wordnet
import sys
import enchant
from nltk import everygrams

def check_spelling(word):
    d = enchant.Dict('en_US')
    try:
        if d.check(word):
            return word.strip()
        else:
            sub_string_arr = sub_string_arr=[''.join(_ngram) for _ngram in everygrams( word) if d.check(''.join(_ngram)) and len(_ngram) > 1]
            word = sub_string_arr [len(sub_string_arr) - 1].strip()
            ''.join(e for e in word if e.isalpha())
            return word
    except:
        return False

def get_synset(word):
    #word = check_spelling(word)
    syns=wordnet.synsets(word)
    syns_length=len(syns)
    if syns_length is 0:
        print ("No Result")
        return None

    print(syns_length)
    definitions=[]
    count=0
    for syn in syns:
        if (count > 4):
            break
        syn_dict={}
        syn_dict['lexname']=syn.lexname().split('.')[0][0] + "."
        syn_dict['definition']=syn.definition()
        definitions.append(syn_dict)
        count=count + 1
    return definitions

# definitions = get_synset("| obstruction $")
# print (definitions)
#print(check_spelling("++++Hello++ AWESOME++"))
