import pandas as pd
import numpy as np
from sympy import re

files = ['24hstore', 'CellPhones', 'clickbuy', 'didongmango', 'Didongthongminh', 'didongviet', 
        'hnammobile', 'hoanghamobile', 'NguyenKim', 'thegioididong']

list = ['url', 'title', 'price', 'pathImg', 'producer', 'chip', 'ram', 'memory']
df = []

def getPathImg(list):
    newList = []
    for path in list:
        try:
            path = path.replace('{', '').replace('}','').split(',')[0].replace('\'', '').replace(' ', '')
        except:
            print(path)
        newList.append(path)
    return newList
    

for file in files:
    data = pd.read_csv('crawlData/rawData/'+file+'.csv')
    data['pathImg'] = getPathImg(data['pathImg'])
    # for item in data['pathImg']:
    #     try:
    #         i = item.index(',')
    #         item = item[0:(i-1)] + "'"
    #         item.remove(",")
    #     except:
    #         pass
    df.append(data[list])

df = pd.concat(df, ignore_index=True)
df.to_csv('crawlData/Data/Data.csv')


