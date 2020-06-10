# !/usr/bin/env python
import os
import time
import utils
import InvertedIndex
import BooleanQuery
import PhraseQuery
import GlobbingQuery
import SpellingCorrect
import Synonyms
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

def prepare():
    print("Preparing...")
    index = utils.get_from_file('index')
    wordlist = utils.get_from_file('wordlist')
    doc_size = utils.get_from_file('doc_size')
    VSM = utils.get_from_file('VSM')
    btree, btree_rev = GlobbingQuery.BuildTree(wordlist)


def main():
    # prepare()
    print("Preparing...")
    index = utils.get_from_file('index')
    wordlist = utils.get_from_file('wordlist')
    doc_size = utils.get_from_file('doc_size')
    VSM = utils.get_from_file('VSM')
    btree, btree_rev = GlobbingQuery.BuildTree(wordlist)
    print("*"*53*2)
    print(" "*34,"This is a simple search engine.")
    print("Support: Bollean query, Wildcard query, Spelling correction, Phrase query and Synonym expansion.")
    print("Also use Top K strategy of static score, VB code index compression strategy and dictionary built by b-tree")
        
    while True:
        print("*"*53*2)
        print("Now you can choose the query mode:")
        print(" "*4,"1. Bollean query")
        print(" "*4,"2. Wildcard query")
        print(" "*4,"3. Spelling correction")
        print(" "*4,"4. Phrase query")
        print(" "*4,"5. Synonym expansion")
        number = input("Input -1 to quit\n")
        if int(number)==-1:
            break
        if int(number) > 5 or int(number) == 0:
            print("Please input 1 to 5 for query and input -1 for quit")
            continue
        query = input("Input your query:\n")

        time_start = time.time()
        if(int(number)==1):
            BooleanQuery.controller(query)

        if(int(number)==2):
            GlobbingQuery.controller(query, btree, btree_rev,wordlist)

        if(int(number)==3):
            SpellingCorrect.spelling_correct(query)

        if(int(number)==4):
            PhraseQuery.phrasequery(query)

        if(int(number)==5):
            Synonyms.synonyms_query(query)

        time_end = time.time()
        print("query time: ", time_end-time_start)



if __name__ == "__main__":
    # initial()
    # prepare()
    main()
