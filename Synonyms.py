import os
import utils
import math
import BooleanQuery
from nltk.corpus import wordnet as wn


def synonyms_query(query):
    queryList = query.split()
    wordList = []
    for i in queryList:
        synonymsSet = wn.synsets(i)
        for setList in synonymsSet:
            for word in setList.lemma_names():
                if (word not in wordList):
                    wordList.append(word)
    # test = str(wordList(1))
    # print(test)
    # print(type(test))
    BooleanQuery.controller(wordList[0])
    # print(wordList)



tmp = "dogs are good friend"
synonyms_query(tmp)





# dog_set = wn.synsets('dog')
# print('dog的同义词集为：', dog_set)
# print('dog的各同义词集包含的单词有：',[dog.lemma_names() for dog in dog_set])
# for dog in dog_set:
    # print(dog.lemma_names())
# print('dog的各同义词集的具体定义是：',[dog.definition() for dog in dog_set])
# print('dog的各同义词集的例子是：',[dog.examples() for dog in dog_set])

