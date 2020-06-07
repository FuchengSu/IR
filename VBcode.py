import os
import utils
import math
import copy

def VBEncodeNumber(n):
    by, byte = '', []
    while True:
        byte.insert(0, n % 128 + 128)
        if n < 128:
            break
        n = n // 128
    for i in range(len(byte)):
        if i < len(byte) - 1:
           by += bin(byte[i]).replace('0b1', '0') + ' '
        else:
           by += bin(byte[i]).replace('0b', '')
    return by


def VBEncode(numbers):
    bytestream = []
    for n in numbers:
        byte = VBEncodeNumber(n)
        bytestream.append(byte)
    return bytestream

def VBDecode(bytestream):
    numbers = []
    n = 0
    for i in range(len(bytestream)):
        byte = bytestream[i].split(' ')
        l = len(byte)
        for j in range(l):
            if j < 1 - 1:
                by = int('0b1' + byte[j][1: len(byte[j])], 2)
            else:
                by = int('0b' + byte[j], 2)
            n = 128*n + by if by < 128 else 128*(n - 1) + by
        numbers.append(n)
        n = 0
    return numbers

def countInvertIndex(daopai):
    daopaidis = daopai.copy()
    for i in range(len(daopai)):
        if i == 0:
            daopaidis[i] = daopai[i]
        else:
            daopaidis[i] = daopai[i] - daopai[i - 1]
    return daopaidis

def countInvert(daopaidis):
    daopai = daopaidis.copy()
    for i in range(len(daopaidis)):
        daopai[i] = sum(daopaidis[0: i + 1])
    return daopai


def create_index():
    index = {}
    indexVB = {}
    doc_size = [0 for d in range(1, utils.D*2+2)] # 21576
    print(len(doc_size))
    files = os.listdir(utils.rpath)
    for file in files:
        content = utils.process_doc_content(utils.rpath+file)
        docID = utils.get_doc_ID(file)

        num = 0 
        for word in content:
            if word not in index:
                doclist = {}
                doclist[docID] = [num]
                index[word] = doclist
                indexVB[word] = copy.deepcopy(doclist)
            else:
                if docID not in index[word]:
                    index[word][docID] = [num]
                else:
                    index[word][docID].append(num)
            num += 1
        doc_size[docID]=num
    
    return index, doc_size


def get_wordlist(index):
    wordlist = []
    for word in index.keys():
        wordlist.append(word)
    
    return wordlist



