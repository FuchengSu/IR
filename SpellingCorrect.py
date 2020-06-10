# encoding: utf-8  
import re, collections
import utils
import PhraseQuery


def tolower(text):

    return re.findall('[a-z]+',text.lower())

def prior(cwords):

    model = collections.defaultdict(lambda:1)
    for f in cwords:
        model[f]+=1
    return model


cwords = utils.get_from_file('wordlist')


def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model
	
#get P(c)
nwords = train(cwords) 


alpha = 'abcdefghijklmnopqrstuvwxyz'
def version1(word):

    n = len(word)
    add_a_char = [word[0:i] + c + word[i:] for i in range(n+1) for c in alpha]
    delete_a_char = [word[0:i] + word[i+1:] for i in range(n)]
    revise_a_char = [word[0:i] + c + word[i+1:] for i in range(n) for c in alpha]
    swap_adjacent_two_chars = [word[0:i] + word[i+1]+ word[i]+ word[i+2:] for i in range(n-1)] 
    return set( add_a_char + delete_a_char +
               revise_a_char +  swap_adjacent_two_chars)
      

def version2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))



def identify(words):
    return set(w for w in words if w in nwords)


def getMax(wanteds):
    threewanteds=[]
    maxword = max(wanteds,key=lambda w : nwords[w])
    threewanteds.append(maxword)
    wanteds.remove(maxword)

    if len(wanteds)>0:
        maxword = max(wanteds,key=lambda w : nwords[w])
        threewanteds.append(maxword)
        wanteds.remove(maxword)
        if len(wanteds)>0:
            maxword = max(wanteds,key=lambda w : nwords[w])
            threewanteds.append(maxword)   
    return threewanteds


def bayesClassifier(word):
    if identify([word]):
        return 0
    wanteds = identify(version1(word)) 
    if len(wanteds)>0:
        return getMax(wanteds)
    wanteds = identify(version2(word))
    if len(wanteds)>0:
        return getMax(wanteds)
    else:    
        return [word + ' not found in dictionary!' ]

def spelling_correct(x):

	y=re.findall(r"\w+",x)
	print("\n")
	number = 0
	query = ""
	for word in y:
		if  bayesClassifier(word)!=0:
			number += 1
			print("The correction of", word, "is as follows:")
			print(bayesClassifier(word))
			query = query + " " + bayesClassifier(word)[0]
	flag = input("Do you want to query as the first correction? (y/n): ")
	if flag == "y":
		print("The corrected query is \"", query, "\"")
		PhraseQuery.phrasequery(query)
