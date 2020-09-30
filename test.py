#! /bin/env/python38

from pprint import pprint
from segmenter.atb import *
from segmenter.util.get_dictionaries import *


sf = get_cedict()

atb = ATB()

for word in sf:
    atb.insert(word, 1)

cases = [
    "中国军方此举是针对当前台海形势和维护国家主权而采取的必要行动",
    "分析人士认为，美国计划同时向台湾进行七项军售，罕见地偏离了多年来美国对台军售的先例。过去，美国对台军售在时间上是隔开的，并经过仔细的校准，以便把与北京的紧张关系降至最低。",
    "台湾总统蔡英文2016年就任台湾总统以来一直拒绝接受北京要求的“九二共识”，以及“一中原则”"
]

def print_segmented(s, compare=False):
    if compare:
        print(s, '\n')
    big = atb.getMatches(s)

    i = 0
    while i < len(big):
        outer = big[i]
        if outer:
            item = max(outer, key=lambda x: len(x[1]))
            print(item[0], end=' | ')
            i += len(item[1])
        else:
            i += 1
    print()
    print('-'*50)

for case in cases:
    print_segmented(case, compare=True)

