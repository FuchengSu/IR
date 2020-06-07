# !/usr/bin/env python
import os
import time
import utils
import InvertedIndex
import BooleanQuery
import PhraseQuery
import GlobbingQuery
import SpellingCorrect
# import Synonyms

def initial():
    index, doc_size = InvertedIndex.create_index()
    wordlist = InvertedIndex.get_wordlist(index)
    VSM = InvertedIndex.create_VSM(index, doc_size, wordlist)
    VSM_sum = InvertedIndex.VSM_sum(VSM)

    utils.write_json(index, utils.ppath+'index.json')
    utils.write_json(wordlist, utils.ppath+'wordlist.json')
    utils.write_json(doc_size, utils.ppath+'doc_size.json')
    utils.write_json(VSM, utils.ppath+'VSM.json')
    utils.write_json(VSM_sum, utils.ppath+'VSM_sum.json')

index = utils.get_from_file('index')
wordlist = utils.get_from_file('wordlist')
doc_size = utils.get_from_file('doc_size')
VSM = utils.get_from_file('VSM')
btree, btree_rev = GlobbingQuery.BuildTree(wordlist)




def main():
    while True:
        number = input("Choose the way to query:\n  1.Boolean Query\n  2.Phrase Query\n  3.Wildcard Query\n  4.Fuzzy Query\nInput 0 to quit\n")
        time_start = time.time()
        if int(number)==0:
            break
        if int(number) > 5 or int(number) < 0:
            print("ERROR")
            continue
        query = input("Input your query:\n")

        if(int(number)==1):
            BooleanQuery.controller(query)

        if(int(number)==2):
            PhraseQuery.phrasequery(query)

        if(int(number)==3):
            GlobbingQuery.controller(query, btree, btree_rev,wordlist)

        if(int(number)==4):
            SpellingCorrect.spelling_correct(query)

        if(int(number)==5):
            Synonyms.synonyms_query(query)

        time_end = time.time()
        print("query time: ", time_end-time_start)



if __name__ == "__main__":
    initial()
    main()
