###TODO: get foreign language dictionary file (CEDICT or similar)
### parse dict into list of words

import string
import operator
import copy
from functools import reduce
from itertools import product


def getDict(dataDict, maplist):
    try:
        return reduce(operator.getitem, maplist, dataDict)
    except:
        return False
        

def setDict(dataDict, maplist, value, x=-1):
    '''Create alpha tree dictionary.
    
    example usage:
    >>> d = {}
    >>> for word in sf: #list of words
            setDict(d, word, word)
    '''
    recall = getDict(dataDict, maplist[:x])
    if recall is False:
        setDict(dataDict, maplist, value, x-1)
    else:
        if x == -1:
            recall.setdefault(maplist[x], {})
            recall[maplist[x]].update( {"$" : 1} )
        else:
            recall.setdefault(maplist[x], {})
            recall[maplist[x]].update({maplist[x+1] : {}})
            setDict(dataDict, maplist, value, x+1)
            
            
def getMatches(alphaDict, s):
    '''Search alphaDict dictionary tree for all possible word matches in string s'''
    sets = []
    all_words = []
    for num1 in range(len(s)):
        for num2 in range(len(s)+1):
            rw = s[num1:num2]
            result = getDict(alphaDict, rw)
            if result and result.get('$'):
                sets.append([rw, range(num1, num2)])
            else:
                if result is False:
                    all_words.append(list(sets))
                    sets.clear()
                    break
                    
    if sets: # any leftover values in sets, append to all_words
        all_words.append(list(sets))
        
    return all_words
