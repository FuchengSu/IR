
import copy
import utils
import json
import chardet
import html
import topk


def phrasequery_wordlist(wordlist):
    docID = []
    docID_storage = []
    judge_index = []
    docID_index = []
    for word in wordlist:
        index = utils.loadLocationIndex(word)
        if index is None:
            print("No such word!")
            return None
        result = []
        for item in index:
            result.append(int(item))
        result.sort()
        storage = {}
        for i in range(len(result)):
            storage.setdefault(i, result[i])
        docID_storage.append(storage)
        docID_index.append(index)
        judge_index.append(0)

    #get common docID
    while True:
        IsSame = True
        IsOver = False
        temp = -1
        max = -1
        for i in range(len(wordlist)):
            if (judge_index[i] >= len(docID_storage[i])):
                IsOver = True
                isSame = False
                break
            if docID_storage[i][judge_index[i]]>max:
                temp = i
                max = docID_storage[i][judge_index[i]]
            if i>0 and IsSame:
                if docID_storage[i][judge_index[i]]!=docID_storage[i-1][judge_index[i-1]]:
                    IsSame=False
        if IsSame:
            if (judge_index[0] >= len(docID_storage[0])):
                break
            docID.append(docID_storage[0][judge_index[0]])
            for i in range(len(wordlist)):
                judge_index[i]+=1
                if(judge_index[i]>=len(docID_storage[i])):
                    IsOver = True
                    break
        else:
            for i in range(len(wordlist)):
                if i!=temp:
                    judge_index[i]+=1
                    if (judge_index[i] >= len(docID_storage[i])):
                        IsOver = True
                        break
        if IsOver:
            break

    #for these docID, judge the location
    result = getPhraseDoc(docID_index, docID)
    return result


def getPhraseDoc(docID_index, docID):
    result = [] #result_docID
    judge_onedoc = [] #wordindex of query words in one doc
    for j in range(len(docID)):
        judge_onedoc = []
        for i in range(len(docID_index)):
            word_index = docID_index[i][str(docID[j])]
            judge_onedoc.append(word_index)
        if(isPhrase(judge_onedoc)):
            result.append(docID[j])
    return result


def isPhrase(judge_onedoc):
    for i in range(len(judge_onedoc)):
        judge_onedoc[i].sort()
    index = 1
    wordlist1 = judge_onedoc[0]
    temp_result = []
    while index<len(judge_onedoc):
        wordlist2 = judge_onedoc[index]
        p1 = 0
        p2 = 0
        while p1<len(wordlist1) and p2<len(wordlist2):
            if(wordlist1[p1]==wordlist2[p2]-1):
                temp_result.append(wordlist2[p2])
                p1+=1
                p2+=1
            elif wordlist1[p1]>wordlist2[p2]:
                p2+=1
            elif wordlist1[p1]<wordlist2[p2]:
                p1+=1
        wordlist1 = temp_result
        index+=1
        if len(wordlist1)==0:
            return False
    if(len(wordlist1)>0):
        return True
    return False

def merge(list1, list2):
    list1.sort()
    list2.sort()
    i = 0
    j = 0
    result = []
    while(i<len(list1) and j<len(list2)):
        if list1[i]==list2[j]:
            result.append(list1[i])
            i+=1
            j+=1
        elif list1[i]<list2[j]:
            i+=1
        else:
            j+=1
    return result

def phrasequery(query):
    query = query.lower()
    wordlist = query.split(' ')
    if len(wordlist) == 2 or len(wordlist) == 1:
        docID = phrasequery_wordlist(wordlist)
    else:
        docID = []
        for i in range(len(wordlist)-1):
            tmpList = []
            tmpList.append(wordlist[i])
            tmpList.append(wordlist[i+1])
            tmpID = phrasequery_wordlist(tmpList)
            if i == 0:
                docID = tmpID
            else:
                docID = merge(docID, tmpID)
    if docID is not None:
        # print("The result is as follows: \n Totally find ",len(docID), " docs.\n")
        # print(docID)
        # flag = input("Do you want to see all docs? (y/n): \n")
        # if flag == "y":
        #     printquery = [query]
        #     newwords = wordlist[0].title()
        #     for i in range(1, len(wordlist)):
        #         newwords += " "+ wordlist[i].title()
        #     printquery.append(newwords)
        #     utils.printtext(printquery,docID)
        # else:
        #     print("query complete\n")
        docID = topk.topK2(wordlist,docID)
        # printquery = [query]
        # newwords = wordlist[0].title()
        # for i in range(1, len(wordlist)):
        #     newwords += " "+wordlist[i].title()
        # printquery.append(newwords)
        # utils.printtext(printquery,docID)



