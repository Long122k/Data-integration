from sklearn.metrics import jaccard_score
from searching import calJaccardMeasure
import pandas as pd
import numpy as np

property = ['index', 'url', 'title', 'price', 'pathImg', 'producer', 'chip', 'ram', 'memory']
list = ['title', 'price', 'producer', 'chip', 'ram', 'memory']

indexs = [2, 3, 5, 6, 7, 8]
weigh = [0.3, 0.2, 0.2, 0.1, 0.1, 0.1]
threshold = 0.9

data = pd.read_csv("CrawlData/Data/data.csv")
data = np.array(data)

def calDistanceRecord(x1, x2):
    distance = 0.0
    for i in range(len(indexs)):
        index = indexs[i]
        jaccard_score = calJaccardMeasure(x1[index], x2[index])
        distance += weigh[i]*jaccard_score
    return distance

def getIndexDuplicate():
    listDuplicate= []
    for i in range(len(data)):
        if i in listDuplicate:
            continue
        for j in range(i+1, len(data)):
            if j in listDuplicate:
                continue
            distance = calDistanceRecord(data[i], data[j])
            if distance > threshold:
                print(i,j)
                listDuplicate.append(j)
    return listDuplicate


def handleDuplicate():
    df = pd.read_csv('crawlData/Data/Data.csv')
    indexs = getIndexDuplicate()
    print("pre data: ", df.shape)
    print("dupliate: ", len(indexs))
    df = df.drop(indexs)
    print("after data: ", df.shape)
    df = pd.concat([df], ignore_index=True)
    df.to_csv('crawlData/Data/newData.csv')

handleDuplicate()





