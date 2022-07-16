import pandas as pd
import numpy as np

df = pd.read_csv('crawlData/Data/newData.csv')
titles = np.array(df['title'])

words = []
for title in titles:
    try:
        list = []
        for token in title.split():
            list.append(token.lower())
        words.append(list)
    except:
         words.append([])

wordSet = set(words[0])
for word in words:
    wordSet = wordSet.union(set(word))

wordDict = []
for i in range(len(titles)):
    wordDict.append(dict.fromkeys(wordSet, 0))

for i in range(len(title)):
    for word in words[i]:
        wordDict[i][word]+=1

def computeTF(wordDict, words):
    tfDict = {}
    wordsCount = len(words)
    for word, count in wordDict.items():
        if wordsCount != 0:
            tfDict[word] = count/float(wordsCount)
        else:
            tfDict[word]  = 0
    return tfDict

def computeIDF(docList):
    import math
    idfDict = {}
    N = len(docList)
    
    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        if val != 0:
            idfDict[word] = math.log10(N / float(val))
        else:
            idfDict[word] = 0
        
    return idfDict

idfs = computeIDF(wordDict)

tfdocs = []
for i in range(len(titles)):
    tfdocs.append(computeTF(wordDict[i], words[i]))

def computeTFIDF(tfDocs, idfs):
    tfidf = {}
    for word, val in tfDocs.items():
        tfidf[word] = val*idfs[word]
    return tfidf

tfidfDoc = []
for i in range(len(titles)):
    tfidf = computeTFIDF(tfdocs[i], idfs)
    tfidfDoc.append(tfidf)

import pandas as pd
df = pd.DataFrame(tfidfDoc)
df.to_csv('crawlData/Data/tf_idf.csv')
