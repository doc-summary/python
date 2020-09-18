#! /bin/env/python38

from segmenter.atb import *
from segmenter.util.get_dictionaries import *

sf = get_cedict()

alpha_dict = dict()

for word in sf:
    setDict(alpha_dict, word, word)
