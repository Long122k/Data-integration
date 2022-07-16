from cmath import nan
import pandas as pd
import numpy as np
from sympy import re

files = ['24hstore', 'CellPhones', 'clickbuy', 'didongmango', 'Didongthongminh', 'didongviet', 
        'hnammobile', 'hoanghamobile', 'NguyenKim', 'thegioididong', 'digiphone', 'mediamart', 'mobilecity', 'viettelstore']

list = ['url', 'title', 'price', 'pathImg', 'producer', 'chip', 'ram', 'memory']

def getPathImg(list):
    newList = []
    for path in list:
        try:
            path = path.replace('{', '').replace('}','').split(',')[0].replace('\'', '').replace(' ', '')
        except:
            print(path)
        newList.append(path)
    return newList
    

def processImgPath():
    df = []
    for file in files:
        data = pd.read_csv('crawlData/rawData/'+file+'.csv')
        data['pathImg'] = getPathImg(data['pathImg'])
        df.append(data[list])
    df = pd.concat(df, ignore_index=True)
    df.to_csv('crawlData/Data/Data.csv')

def dropMissingData():
    df = pd.read_csv('crawlData/Data/Data.csv')
    indexs = []
    i = 0
    for obj in df['price']:
        if issubclass(type(obj), float):
            indexs.append(i)
        i += 1
    
    df = df.drop(indexs)
    print(df.shape)
    df = pd.concat([df], ignore_index=True)
    df.to_csv('crawlData/Data/Data.csv')

dropMissingData()
