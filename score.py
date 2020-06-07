import os
import math

import utils
import InvertedIndex
import BooleanQuery

def cosinescore(Qlist,docID):
	print(docID)
	VSM = utils.get_from_file('VSM')
	Wordlist = utils.get_from_file('wordlist')
	Qworddic = {}
	QLen = len(Qlist)
	q_tf_idf = []
	s_length = 0
	length = 0
	for Qword in Qlist:
		if Qword not in Qworddic:
			Qworddic[Qword] = 1
		else:
			Qworddic[Qword] += 1
	for Qword in Qworddic:
		s_length += pow(Qworddic[Qword],2)
	length = math.sqrt(s_length)
	for Qword in Qworddic:
		Qworddic[Qword] = Qworddic[Qword]/length 

	doc_magnitude_0 = VSM[str(docID)]
	doc_magnitude_1 = []
	for score in doc_magnitude_0:
		if float(score) < 1:
			doc_magnitude_1.append(score)
		else:
			for i in range(int(score)):
				doc_magnitude_1.append('0.0')
	Dworddic = {}
	for Qword in Qworddic:
		for i in range(0,len(Wordlist)):
			if Qword == Wordlist[i]:
				Dworddic[Qword] = doc_magnitude_1[i] 
				break
		print(i)
	result = 0
	for Qword in Qworddic:
		result += float(Qworddic[Qword]) * float(Dworddic[Qword])
	c_score = '%.20f' % float(doc_magnitude_1[i]) 
	print(Qworddic)
	print(Dworddic)
	print(c_score)
	return c_score
