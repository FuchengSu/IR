import os
import utils
import math


def create_index():
    index = {}
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

# TF_word_i = len(index[word][article_i])/doc_size[article_i]
# IDF = log_2(D/len(index[word])), D=10788
# TF-IDF_word_i = TF*IDF
def create_VSM(index, doc_size, wordlist):
    index = utils.get_from_file('index')
    VSM = {}
    for d in range(1, utils.D*2+1): # 21576
        if d % 1000 == 0:
            print('Processing:'+str(d))
        if doc_size[d]==0:
            continue
        tf_idf_list = []
        num = 0
        for word in wordlist:
            if str(d) not in index[word]:
                num += 1
            else:
                tf = float(1 + math.log2(len(index[word][str(d)])))
                # tf = float(len(index[word][str(d)])/doc_size[d])
                # print(word)
                # ttt = input()
                idf = math.log2(utils.D/len(index[word]))
                tf_idf = '%.3f' % float(tf*idf) 
                tf_idf_list.append([num,tf_idf])
                num = 1
        VSM[d] = tf_idf_list

    return VSM


def VSM_sum(VSM):
    sum_VSM = {}
    for d in range(1, utils.D*2+1): # 21576
        if d % 1000 == 0:
            print('Processing'+str(d))
        if d in VSM.keys():
            sum = 0.0
            temp = VSM[d]
            for tfidf in temp:
                sum += float(tfidf[1])**2
            for tfidf in temp:
                tfidf[1] = str(float(tfidf[1])/sum)
            sum_VSM[d] = temp
        #    print(VSM[str(d)])
        #    print(sum_VSM[d])
    
    return sum_VSM

# def VSM_sum(VSM):
#     sum_VSM = {}
#     for d in range(1, utils.D*2+1): # 21576
#         if d % 1000 == 0:
#             print('Processing'+str(d))
#         if str(d) in VSM.keys():
#             sum = 0.0
#             for tfidf in VSM[str(d)]:
#                 if float(tfidf) < 1:
#                     sum += float(tfidf)
#             sum_VSM[d] = '%.3f' % sum
    
#     return sum_VSM