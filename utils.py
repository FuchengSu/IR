import os
import json
from nltk import word_tokenize
import chardet
import tokenize
import html


ppath = os.getcwd()+'/'
rpath = ppath + 'Reuters/'
D = 10788 


def write_json(data, filename):
    file = open(filename, 'w')
    str = json.JSONEncoder().encode(data)
    file.write(str)
    file.close()


def get_doc_list():
    filelist = []
    files = os.listdir('./Reuters/')
    for file in files:
        filelist.append(get_doc_ID(file))
    return sorted(filelist)


def get_doc_ID(filename):
    docID = os.path.splitext(filename)[0]
    return int(docID)


def process_doc_content(filename):
    with open(filename, 'r', encoding='ISO-8859-1') as file:
        content = file.read()
    res = []
    result = []
    punc_digit = [',', '.', ';', ':', '&', '>', "'", '"','`', '+', '*', '?', '!', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for word in word_tokenize(content):
        word = word.lower()
        for c in punc_digit:
            word = word.replace(c, '')
        if len(word) == 0 or word[0] == '-':
            continue
        if word[0] == '\'':
            continue
        if word.find('/') > 0:
            res = word.split('/')
            for w in res:
                result.append(w)
            continue
        result.append(word)
    return result

def get_from_file(filename):
    file = open(filename+'.json', 'r')
    res = json.JSONDecoder().decode(file.read())
    return res

def loadLocationIndex(word):
    f = open("index.json", encoding='utf-8')
    dictionary = json.load(f)
    index = dictionary[word]
    return index


def loadIndex(word):
    f = open("index.json", encoding='utf-8')
    dictionary = json.load(f)
    index = dictionary[word]
    result = []
    for item in index:
        result.append(int(item))
    return result

def printtext(wordlist, doclist):
    directory = "./Reuters"
    highlights = []
    for word in wordlist:
        highlights.append(word)
        highlights.append(word.upper())
        highlights.append(word.title())
    for docid in doclist:
        with open(directory + '/' + str(docid) + '.html', 'rb') as htmlfile:
            rawdata = htmlfile.read()
            encoding = chardet.detect(
                rawdata)['encoding']
            text = rawdata.decode(encoding)
            text = html.unescape(text)
        print("************** Boolean Query Result **************")
        print("\033[1;33;40m"+str(docid)+".html"+"\033[0m")
        for word in highlights:
            text = text.replace(word, "\033[1;31;40m" + word + "\033[0m")
        print(text)
