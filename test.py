import os
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



index = {}
index2 = {}
doclist = {}
doclist[12345] = [1]
index['zys'] = doclist
index2['zys'] = copy.deepcopy(doclist)
# index2 = copy.deepcopy(index)
index['zys'][23456] = [23]
index['zys'][34567] = [2]
index['zys'][12345].append(4)
index['zys'][12345].append(10)
doclist = {}
doclist[4478] = [4]
index['wwj'] = doclist
index2['wwj'] = copy.deepcopy(doclist)
index['wwj'][4567] = [12]
index['wwj'][4569] = [2]
     
# daopaidis = VBDecode(bytestream)
# daopai = countInvert(daopaidis)
VBlist = []
for key in index:
    # print(list(index[key]))
    daopaidis = countInvertIndex(list(index[key]))
    bytestream = VBEncode(daopaidis)
    index2[key] = []
    # tmp = {}
    tmplist = []
    tmpi = 0
    for (key2, value) in index[key].items():
        tmpdict = {}
        tmpdict[bytestream[tmpi]] = value
        index2[key].append(tmpdict)
        tmpi += 1
        
    
    # tmp = dict(zip(bytestream, tmplist))
    # index2[key] = copy.deepcopy(tmp)

def sub(string, p, c):
    new = []
    for s in string:
        new.append(s)
    new[p] = c
    return ''.join(new)

temp = str(index2)
print(index2)   
zhuangtai = 0   
i = 0
ttt = ''
for i in range(len(temp)):
    if temp[i] == '[' and zhuangtai == 0:
        zhuangtai = 1
        ttt = ttt + '{'
    elif temp[i] == '{' and zhuangtai == 1:
        zhuangtai = 2
        # temp = temp[:i] + temp[i+1:]
    elif temp[i] == '}' and zhuangtai == 2:
        # temp = temp[:i] + temp[i+1:]
        zhuangtai = 3
    elif temp[i] == ']' and zhuangtai == 3:
        zhuangtai = 0
        ttt = ttt + '}'
    elif temp[i] != ']' and zhuangtai == 3:
        zhuangtai = 1
        ttt = ttt + temp[i]
    else:
        ttt = ttt + temp[i]


print(index)
print(ttt)  
# print(type(temp))
# print(index2)
# print(type(index2))
