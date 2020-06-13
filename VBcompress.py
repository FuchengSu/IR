import os
import math
import copy
import sys
import json

by = []

def VBEncodeNumber(n):
    byte = []
    while True:
        byte.insert(0, n % 128)
        if n < 128:
            break
        n = n // 128
    byte[len(byte)-1] += 128
    by.extend(byte)

def VBEncode(numbers):
    for n in numbers:
        VBEncodeNumber(n)
    bytestream = bytes(by)
    by.clear()
    return bytestream

def VBDecode(bytestream):
    numbers = []
    n = 0
    for i in range(len(bytestream)):
        if bytestream[i] < 128:
            n = 128 * n + bytestream[i]
        else:
            n = 128 * n + bytestream[i] - 128
            numbers.append(n)
            n = 0
    return numbers

def loadIndex(word):
    f = open('index.json', encoding='utf-8')
    dictionary = json.load(f)
    index = dictionary[word]
    result = []
    for item in index:
        result.append(int(item))
    return result

def loadLocationIndex(word):
    f = open('index.json', encoding='utf-8')
    dictionary = json.load(f)
    index = dictionary[word]
    return

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

def write_json(data, filename):
    file = open(filename, 'w')
    str = json.JSONEncoder().encode(data)
    file.write(str)
    file.close()

def compress(file_compress,file_store):
    new_index = {}
    f = open(file_compress, encoding='utf-8')
    dictionary = json.load(f)

    for dic in dictionary:
        index = dictionary[dic]
        temp = []
        sub_index = []
        for key in sorted(index.keys(), key=lambda s: int(s)):
            sub_index.append(int(key))
        daopaidis = countInvertIndex(sub_index)
        bytestream = VBEncode(daopaidis)
        temp.append(int.from_bytes(bytestream, byteorder='big', signed=False))
        for key in sorted(index.keys(), key=lambda s: int(s)):
            daopaidis = countInvertIndex(list(index[key]))
            bytestream = VBEncode(daopaidis)
            temp.append(int.from_bytes(bytestream, byteorder='big', signed=False))
        new_index[dic] = temp
    write_json(new_index, file_store)
    f.close()

def decompress(file_decompress,file_store):
    num = 1
    dictionary2 = {}
    f2 = open(file_decompress, encoding='utf-8')
    dictionary2 = json.load(f2)
    new_index2 = {}

    for dic in dictionary2:
        daopaidis = []
        daopai = []
        temp = {}
        index = dictionary2[dic]
        temp_byte = int.to_bytes(index[0], 10000, byteorder='big', signed=False)
        daopaidis = VBDecode(temp_byte)
        daopai = countInvert(daopaidis)

        for i in range(len(index) - 1):
            locationdis = []
            location = []
            bytestream = int.to_bytes(index[i + 1], 10000, byteorder='big', signed=False)
            locationdis = VBDecode(bytestream)
            location = countInvert(locationdis)
            temp[daopai[i]] = location

        new_index2[dic] = temp
        print(num)
        num = num + 1

    f2.close()
    write_json(new_index2, file_store)

# compress('index.json','indexcompress')
# decompress('indexcompress', 'newindex.json')

# fsize1 = os.path.getsize('index.json')
# fsize2 = os.path.getsize('indexcompress')
# fsize3 = os.path.getsize('newindex.json')
# print(fsize1)
# print(fsize2)
# print(fsize3)