import utils
import cmath
import queue

class PriorityQueue:
    def __init__(self, scoreDocList, N, K):
        self.data = scoreDocList
        self.n = N
        self.k = K

    def percDown(self, start, end):
        now = self.data[start]
        while 2*start+1 < end:
            child = 2*start+1
            if child != end-1 and self.data[child+1][0] > self.data[child][0]:
                child += 1
            if now[0] < self.data[child][0]:
                self.data[start] = self.data[child]
            else:
                break
            start = child
        self.data[start] = now

    def sort(self):
        mid = int(self.n/2)
        while mid >= 0:
            self.percDown(mid, self.n)
            mid -= 1
        mid = self.n - 1
        end = 0
        if self.n - 1 > self.k:
            end = self.n - 1 - self.k
        while mid > end:
            temp = self.data[0]
            self.data[0] = self.data[mid]
            self.data[mid] = temp
            self.percDown(0, mid)
            mid -= 1

def searchWords(wordList, index):
    if len(wordList) == 0:
        return []
    docID = []
    for word in wordList:
        if word not in index:
            continue
        for key in index[word]:
            docID.append(int(key))
    docID = list(set(docID))
    return docID

def getScore(index, doc, wordList, VSM, wordict):
    AB = 0
    A = 1
    B = 1
    doc = str(doc)
    now = 0
    print(VSM[doc])
    for i in range(len(VSM[doc])//2):
        now += int(VSM[doc][2*i])
        if wordict[now] in wordList:
            q = VSM[doc][2*i+1]
            AB += wfidf/(len(wordList)**0.5)
            A *= wfidf**2
            B *= 1/len(wordList)

    return AB/((A*B)**0.5)

def topK(wordlist, index):
    if type(wordlist) != list:
        wordlist = wordlist.strip(' ').split(' ')

    docID = searchWords(wordlist, index)
    print("The result is as follows: \n Totally find ",len(docID), " docs.\n")
    flag = input("Do you want to see all docs? (y/n): ")
    if flag == "y":
        K = -1
    else:
        K = int(input("How many docs do you want to see? (topK)\n"))
    if len(docID) < K or K == -1:
        K = len(docID)
    scoreDocList = []
    VSM = utils.get_from_file('VSM')
    wordict = utils.get_from_file('wordlist')
    VSM_sum = utils.get_from_file('VSM_sum')
    for doc in docID:
        scoreDocList.append([getScore(index, doc, wordlist, VSM, wordict)+0.01*VSM_sum[doc], doc])

    pq = PriorityQueue(scoreDocList,len(docID),K)
    pq.sort()
    result = [pq.data[len(docID)-x-1] for x in range(0,K)]

    # print("\n\n************* Show Result ************\n\nFind ",len(docID), " docs.\n")
    print("Show ", len(result), " docs.\n")
    for doc in result:
        print("docID: ", doc[1], ", score: ",doc[0])
    stop = input("\nPress any key to show articles...\n")
    return result    


def topK2(wordlist, docID):
    print("The result is as follows: \n Totally find ",len(docID), " docs.\n")
    flag = input("Do you want to see all docs? (y/n): ")
    if flag == "y":
        K = -1
    else:
        K = int(input("How many docs do you want to see? (topK)\n"))
    if len(docID) < K or K == -1:
        K = len(docID)
    index = utils.get_from_file('index')
    scoreDocList = []
    for doc in docID:
        scoreDocList.append([getWfidfScore(index, doc, wordlist), doc])
    pq = PriorityQueue(scoreDocList,len(docID),K)
    pq.sort()
    result = [pq.data[len(docID)-x-1] for x in range(0,K)]
    for doc in result:
        print("docID: ", doc[1], ", score: ",doc[0])
    return result
