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

def getWfidfScore(index, doc, wordList):
    score = 0
    doc = str(doc)
    for word in wordList:
        if word not in index or doc not in index[word]:
            continue
        tf = len(index[word][doc])
        wf = 1 + cmath.log10(tf).real
        df = len(index[word])
        idf = cmath.log10(utils.D/df).real
        score += wf * idf
    return score

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
    for doc in docID:
        scoreDocList.append([getWfidfScore(index, doc, wordlist), doc])

    pq = PriorityQueue(scoreDocList,len(docID),K)
    pq.sort()
    result = [pq.data[len(docID)-x-1] for x in range(0,K)]

    # print("\n\n************* Show Result ************\n\nFind ",len(docID), " docs.\n")
    print("Show ", len(result), " docs.\n")
    for doc in result:
        print("docID: ", doc[1], ", score: ",doc[0])
    stop = input("\nPress any key to show articles...\n")
    return result    
